import csv
import os
import sys

sys.path.insert(0, os.getcwd())

from research_uet.lab.galaxies.test_175_galaxies_v4 import SPARC_GALAXIES


def recover():
    output_path = "research_uet/data_vault/sources/sparc_175.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "R_kpc", "v_obs", "M_disk_Msun", "R_disk_kpc", "type"])
        writer.writerows(SPARC_GALAXIES)

    print(f"Recovered {len(SPARC_GALAXIES)} records to {output_path}")


if __name__ == "__main__":
    recover()
