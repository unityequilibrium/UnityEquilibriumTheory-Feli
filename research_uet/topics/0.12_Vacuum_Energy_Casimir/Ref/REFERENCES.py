"""
REFERENCES.py - 0.12 Vacuum Energy & Casimir
=============================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "Casimir_Force": {
            "title": "Precision Measurement of the Casimir Force from 0.1 to 0.9 μm",
            "authors": ["Mohideen, U.", "Roy, A."],
            "journal": "Physical Review Letters",
            "volume": 81,
            "pages": "4549",
            "year": 1998,
            "doi": "10.1103/PhysRevLett.81.4549",
        },
        "Planck_2018_DE": {
            "title": "Planck 2018 Results. VI. Cosmological Parameters",
            "authors": ["Planck Collaboration"],
            "journal": "Astronomy & Astrophysics",
            "volume": 641,
            "pages": "A6",
            "year": 2020,
            "doi": "10.1051/0004-6361/201833910",
        },
    }
}


def print_references():
    print("0.12 Vacuum Energy & Casimir - References")
    for name, ref in REFERENCES["primary"].items():
        print(f"📚 {name}: DOI {ref['doi']}")


if __name__ == "__main__":
    print_references()
