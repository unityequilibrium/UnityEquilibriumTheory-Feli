import os
import subprocess
import sys
from pathlib import Path


def main():
    print("UET TARGETED PROOF VERIFICATION")
    print("==================================")

    # Identify proofs
    root = Path(__file__).resolve().parent
    proofs = sorted(list(root.glob("research_uet/topics/*/Code/02_Proof/Proof_*.py")))

    if not proofs:
        print("No Proof scripts found!")
        return

    passed = 0
    failed = []

    for p in proofs:
        rel_path = p.relative_to(root)
        print(f"Running {rel_path}...")

        try:
            result = subprocess.run(
                [sys.executable, str(p)], capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and "PASS" in result.stdout:
                print(f"  PASS")
                passed += 1
            else:
                print(f"  FAIL")
                failed.append(str(rel_path))
                if result.stderr:
                    print(f"    Error: {result.stderr[:200]}")
                elif "FAIL" in result.stdout:
                    print(f"    Failure captured in stdout.")
        except Exception as e:
            print(f"  CRASH: {e}")
            failed.append(str(rel_path))

    print("\n==================================")
    print(f"RESULT: {passed}/{len(proofs)} Passed")
    print("==================================")

    if failed:
        print("\nFailed Proofs:")
        for f in failed:
            print(f" - {f}")
        sys.exit(1)
    else:
        print("\n ALL PROOFS VERIFIED PURE ")
        sys.exit(0)


if __name__ == "__main__":
    main()
