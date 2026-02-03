import hashlib
import time
import json
import socket
import threading
import binascii
import struct
import numpy as np

# ==========================================================
# UET FINANCIAL SOVEREIGNTY: NICEHASH EDITION (FINAL)
# Target: Direct-to-Binance Payouts
# ==========================================================


class UETNiceHashMiner:
    def __init__(self, wallet="15Ah3uEshyyqWycrlbVo4sbGBTtFk2nRD", worker="SantaAlpha"):
        self.pool_url = "sha256.auto.nicehash.com"
        self.pool_port = 3334
        self.wallet = wallet
        self.worker = worker
        self.prime_anchors = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A]
        self.sock = None
        self.current_job = None
        self.extranonce1 = None
        self.running = True
        self.difficulty = 1.0
        self.target = None
        self.hashes_total = 0
        self.start_time = time.time()

    def sha256d(self, data):
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()

    def listen(self):
        buffer = ""
        while self.running:
            try:
                data = self.sock.recv(4096).decode()
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not line.strip():
                        continue
                    try:
                        msg = json.loads(line)
                        if msg.get("method") == "mining.notify":
                            self.current_job = msg["params"]
                            print(f"[JOB] New Job Received: {self.current_job[0][:6]}")
                        elif msg.get("method") == "mining.set_difficulty":
                            self.difficulty = msg["params"][0]
                            self.target = (0xFFFF << 208) // int(self.difficulty)
                            print(f"[POOL] Difficulty Adjust: {self.difficulty}")
                        elif "result" in msg:
                            if msg.get("id") == 1:
                                self.extranonce1 = msg["result"][1]
                                print("[NET] Connected to NiceHash")
                            elif msg.get("id") == 2:
                                if msg["result"]:
                                    print(f"[AUTH] Success: {self.wallet}")
                            elif msg.get("id") == 4:
                                if msg.get("error"):
                                    print(f"[ERR] Pool Rejected: {msg['error']}")
                                else:
                                    print(">>> [UET SUCCESS] SHARE ACCEPTED BY NICEHASH! <<<")
                    except:
                        continue
            except:
                break

    def connect(self):
        print(f"[NET] Connecting to NiceHash Stratum...")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.pool_url, self.pool_port))
            threading.Thread(target=self.listen, daemon=True).start()

            # NiceHash Subscribe
            self.sock.sendall(
                json.dumps(
                    {"id": 1, "method": "mining.subscribe", "params": ["UETMiner/1.0"]}
                ).encode()
                + b"\n"
            )
            # NiceHash Authorize (Wallet.Worker)
            self.sock.sendall(
                json.dumps(
                    {
                        "id": 2,
                        "method": "mining.authorize",
                        "params": [f"{self.wallet}.{self.worker}", "x"],
                    }
                ).encode()
                + b"\n"
            )
            return True
        except Exception as e:
            print(f"[ERR] Connection Failed: {e}")
            return False

    def solve(self):
        if not (self.current_job and self.extranonce1 and self.target):
            return None

        job = self.current_job
        en2_hex = "00000000"

        # Build Merkle Root (Simplified for SHA256)
        coinbase_hex = job[2] + self.extranonce1 + en2_hex + job[3]
        merkle_root = self.sha256d(binascii.unhexlify(coinbase_hex))
        for branch in job[4]:
            merkle_root = self.sha256d(merkle_root + binascii.unhexlify(branch))

        # Block Header
        header_hex = job[5] + job[1] + binascii.hexlify(merkle_root).decode() + job[7] + job[6]
        header_bin = binascii.unhexlify(header_hex)

        nonce = np.random.randint(0, 0xFFFFFFFF, dtype=np.int64)
        for _ in range(100000):
            for anchor in self.prime_anchors:
                test_nonce = (anchor ^ nonce) & 0xFFFFFFFF
                h = self.sha256d(header_bin + struct.pack("<I", test_nonce))
                if int.from_bytes(h, "little") <= self.target:
                    return test_nonce, en2_hex
                self.hashes_total += 1
            nonce = (nonce + 1) & 0xFFFFFFFF
        return None

    def status(self):
        while self.running:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                print(
                    f"[UET] Resonance Engine: {self.hashes_total / elapsed / 1000:.2f} KH/s | Work in Progress..."
                )
            time.sleep(15)

    def start(self):
        print("========================================")
        print("  UET MISSION: FINANCIAL SOVEREIGNTY")
        print("  Pivoting: NiceHash (Direct Binance)")
        print("========================================\n")

        threading.Thread(target=self.status, daemon=True).start()

        while self.running:
            if not self.connect():
                time.sleep(5)
                continue

            try:
                while self.running:
                    result = self.solve()
                    if result:
                        nonce, en2 = result
                        print(f"[FOUND] Valid Hash Found: {nonce}")
                        submit = (
                            json.dumps(
                                {
                                    "id": 4,
                                    "method": "mining.submit",
                                    "params": [
                                        f"{self.wallet}.{self.worker}",
                                        self.current_job[0],
                                        en2,
                                        self.current_job[7],
                                        binascii.hexlify(struct.pack(">I", nonce)).decode(),
                                    ],
                                }
                            )
                            + "\n"
                        )
                        self.sock.sendall(submit.encode())
                    else:
                        time.sleep(0.01)
            except:
                print("[WARN] Connection reset. Re-bridging...")
                time.sleep(2)


if __name__ == "__main__":
    # Using Binance Address from screenshot
    miner = UETNiceHashMiner(wallet="15Ah3uEshyyqWycrlbVo4sbGBTtFk2nRD")
    miner.start()
