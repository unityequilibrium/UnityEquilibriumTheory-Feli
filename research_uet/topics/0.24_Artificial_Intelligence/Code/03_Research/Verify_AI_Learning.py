"""
Verify_AI_Learning.py
=====================
Grand Production Upscale: Verification of Topic 0.24.
Checks if UET Cortex Engine (V4.0) can actually learn Non-Linear Logic (XOR)
via Gradient Descent with Entropy Regularization.

Target:
    1. Loss Convergence (< 0.1)
    2. XOR Accuracy (100%)
"""

import sys
import numpy as np
from pathlib import Path

# Path Fix
current_path = Path(__file__).resolve()
# Go up to 'research_uet' parent
root_path = current_path.parents[5]
sys.path.append(str(root_path))

# Local Import
engine_dir = current_path.parents[1] / "01_Engine"
sys.path.append(str(engine_dir))

from UET_AI_Core import UetcortexNeuralNet
from research_uet.core.uet_parameters import UETParameters


def run_verification():
    print("🧠 UET CORTEX AI: PRODUCTION VERIFICATION")
    print("=========================================")
    print("Target: XOR Logic Gate (Non-Linear Learning)\n")

    # 1. Setup Data (XOR)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])  # XOR Truth Table

    # 2. Initialize Engine (Entropy Pressure = 0.001 to allow learning)
    params = UETParameters(kappa=0.1, beta=0.001)
    net = UetcortexNeuralNet(input_size=2, hidden_size=6, output_size=1, params=params)

    print("  [1] Training (Backpropagation)...")
    epochs = 5000
    for i in range(epochs):
        loss = net.train_step(X, y, learning_rate=0.5)
        if i % 1000 == 0:
            print(f"      Epoch {i}: Loss = {loss:.5f}")

    final_loss = net.loss_history[-1]
    print(f"      Final Loss: {final_loss:.5f}")

    # 3. Verify Predictions
    print("\n  [2] Testing Predictions")
    preds = net.forward(X)
    rounded = np.round(preds)

    # Accuracy
    accuracy = np.mean(rounded == y) * 100

    for i in range(4):
        print(f"      Input {X[i]} -> Pred {preds[i][0]:.4f} (Target {y[i][0]})")

    print(f"\n      Accuracy: {accuracy:.2f}%")

    if accuracy == 100.0 and final_loss < 0.1:
        print("\n✅ STATUS: SUCCESS (Genuine Gradient Descent Confirmed)")
        print("   The network learned the XOR function from scratch.")
    else:
        print("\n❌ STATUS: FAILED (Did not converge)")


if __name__ == "__main__":
    run_verification()
