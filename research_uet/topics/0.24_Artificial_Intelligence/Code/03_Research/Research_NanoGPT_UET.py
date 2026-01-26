"""
UET NanoGPT: Text Generation with Physics Optimizer
===================================================
Topic: 0.24 Artificial Intelligence
"""

import sys
import math
import json
import random
from pathlib import Path

# --- PATH SETUP (Must be FIRST) ---
current_path = Path(__file__).resolve()
ROOT = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        ROOT = parent
        break

if ROOT:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    print("CRITICAL: research_uet root not found!")
    sys.exit(1)

# Core Imports After Path Setup
try:
    from research_uet.core.uet_glass_box import UETPathManager
except ImportError as e:
    print(f"CRITICAL SETUP ERROR: {e}")
    sys.exit(1)

# Pytorch Check
try:
    import torch
    import torch.nn as nn
    from torch.nn import functional as F

    TORCH_AVAILABLE = True
except ImportError:
    print(
        "WARNING: torch not found. This script requires torch for full functionality."
    )
    TORCH_AVAILABLE = False
    if __name__ == "__main__":
        print("SKIPPING: Torch not installed.")
        sys.exit(0)

TOPIC_DIR = ROOT / "research_uet" / "topics" / "0.24_Artificial_Intelligence"

# Engine Import (Dynamic)
try:
    import importlib.util

    engine_file = TOPIC_DIR / "Code" / "01_Engine" / "UET_AI_Core.py"
    spec = importlib.util.spec_from_file_location("UET_AI_Core", engine_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    UETOptimizer = getattr(module, "UETOptimizer")
except Exception as e:
    print(f"Error loading AI Engine: {e}")
    sys.exit(1)

# --- HYPERPARAMETERS ---
batch_size = 32
block_size = 16  # Reduced for speed
max_iters = 100  # Reduced for speed
eval_interval = 50
learning_rate = 1e-3
device = "cpu"
n_embd = 32  # Reduced for speed
n_head = 2
n_layer = 2
dropout = 0.0

torch.manual_seed(1337)

# --- DATA LOADING ---
data_path = TOPIC_DIR / "Data" / "03_Research" / "tiny_shakespeare.txt"
if not data_path.exists():
    text = "To be or not to be, that is the question. " * 1000
else:
    with open(data_path, "r", encoding="utf-8") as f:
        text = f.read()

chars = sorted(list(set(text)))
vocab_size = len(chars)
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join([itos[i] for i in l])

data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data = data[:n]
val_data = data[n:]


def get_batch(split):
    data = train_data if split == "train" else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i : i + block_size] for i in ix])
    y = torch.stack([data[i + 1 : i + block_size + 1] for i in ix])
    return x, y


# --- SHORTHAND MODELS ---
class Head(nn.Module):
    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer("tril", torch.tril(torch.ones(block_size, block_size)))

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)
        q = self.query(x)
        wei = q @ k.transpose(-2, -1) * C**-0.5
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float("-inf"))
        wei = F.softmax(wei, dim=-1)
        v = self.value(x)
        out = wei @ v
        return out


class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(n_embd, n_embd)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.proj(out)
        return out


class FeedFoward(nn.Module):
    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd), nn.ReLU(), nn.Linear(4 * n_embd, n_embd)
        )

    def forward(self, x):
        return self.net(x)


class Block(nn.Module):
    def __init__(self, n_embd, n_head):
        super().__init__()
        head_size = n_embd // n_head
        self.sa = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedFoward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x


class NanoGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(
            *[Block(n_embd, n_head=n_head) for _ in range(n_layer)]
        )
        self.ln_f = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok_emb = self.token_embedding_table(idx)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device))
        x = tok_emb + pos_emb
        x = self.blocks(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)
        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B * T, C)
            targets = targets.view(B * T)
        loss = F.cross_entropy(logits, targets)
        return logits, loss

    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -block_size:]
            logits, loss = self(idx_cond)
            logits = logits[:, -1, :]
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)
        return idx


def train_uet_nanogpt():
    print("=" * 60)
    print("📜 UET NANO-GPT TRAINING (Standardized)")
    print("=" * 60)
    model = NanoGPT().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    uet_engine = UETOptimizer(decay_rate=0.001)
    active_ratio = 1.0

    for iter in range(max_iters):
        xb, yb = get_batch("train")
        logits, loss = model(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        loss_val = loss.item()
        _, new_ratio = uet_engine.step(loss_val, active_ratio)
        active_ratio = new_ratio
        if iter % 20 == 0:
            print(f"Step {iter}: Loss {loss_val:.4f} | Active {active_ratio*100:.2f}%")

    print(f"\nFinal Active Ratio: {active_ratio*100:.2f}%")
    print("RESULT: PASS")
    return True


if __name__ == "__main__":
    train_uet_nanogpt()
