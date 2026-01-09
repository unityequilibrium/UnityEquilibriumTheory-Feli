"""
REFERENCES.py - 0.6 Electroweak Physics
========================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "PDG_2024": {
            "title": "Review of Particle Physics",
            "authors": ["Particle Data Group"],
            "journal": "Progress of Theoretical and Experimental Physics",
            "year": 2024,
            "doi": "10.1093/ptep/ptac097",
        },
        "W_Mass_CDF": {
            "title": "High-precision measurement of the W boson mass with the CDF II detector",
            "authors": ["CDF Collaboration"],
            "journal": "Science",
            "volume": 376,
            "pages": "170",
            "year": 2022,
            "doi": "10.1126/science.abk1781",
        },
    },
    "supplementary": [
        {
            "name": "Higgs Discovery",
            "title": "Observation of a new particle in the search for the Standard Model Higgs boson",
            "doi": "10.1016/j.physletb.2012.08.021",
            "year": 2012,
        },
        {
            "name": "Sin2 Theta W",
            "title": "Precision electroweak measurements",
            "doi": "10.1103/PhysRevD.98.030001",
            "year": 2018,
        },
    ],
}


def print_references():
    print("0.6 Electroweak Physics - References")
    for name, ref in REFERENCES["primary"].items():
        print(f"📚 {name}: DOI {ref['doi']}")


if __name__ == "__main__":
    print_references()
