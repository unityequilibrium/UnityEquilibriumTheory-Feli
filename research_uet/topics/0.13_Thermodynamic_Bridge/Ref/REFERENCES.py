"""
REFERENCES.py - 0.13 Thermodynamic Bridge
==========================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "Landauer_Berut": {
            "title": "Experimental verification of Landauer's principle",
            "authors": [
                "Bérut, A.",
                "Arakelyan, A.",
                "Petrosyan, A.",
                "Ciliberto, S.",
                "Dillenschneider, R.",
                "Lutz, E.",
            ],
            "journal": "Nature",
            "volume": 483,
            "pages": "187",
            "year": 2012,
            "doi": "10.1038/nature10872",
        },
        "Bekenstein_Bound": {
            "title": "Universal upper bound on the entropy-to-energy ratio for bounded systems",
            "authors": ["Bekenstein, J.D."],
            "journal": "Physical Review D",
            "volume": 23,
            "pages": "287",
            "year": 1981,
            "doi": "10.1103/PhysRevD.23.287",
        },
    },
    "supplementary": [
        {
            "name": "Jacobson",
            "title": "Thermodynamics of Spacetime: The Einstein Equation of State",
            "doi": "10.1103/PhysRevLett.75.1260",
            "year": 1995,
        }
    ],
}


def print_references():
    print("0.13 Thermodynamic Bridge - References")
    for name, ref in REFERENCES["primary"].items():
        print(f"📚 {name}: DOI {ref['doi']}")


if __name__ == "__main__":
    print_references()
