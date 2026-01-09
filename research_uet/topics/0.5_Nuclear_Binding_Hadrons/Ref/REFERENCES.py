"""
REFERENCES.py - 0.5 Nuclear Binding & Hadrons
==============================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "AME2020": {
            "title": "The AME 2020 atomic mass evaluation",
            "authors": [
                "Wang, M.",
                "Huang, W.J.",
                "Kondev, F.G.",
                "Audi, G.",
                "Naimi, S.",
            ],
            "journal": "Chinese Physics C",
            "volume": 45,
            "pages": "030003",
            "year": 2021,
            "doi": "10.1088/1674-1137/abddaf",
        },
        "PDG_2024": {
            "title": "Review of Particle Physics",
            "authors": ["Particle Data Group"],
            "journal": "Progress of Theoretical and Experimental Physics",
            "year": 2024,
            "doi": "10.1093/ptep/ptac097",
        },
    },
    "supplementary": [
        {
            "name": "Proton Radius",
            "title": "Proton Radius Puzzle",
            "doi": "10.1038/nature09250",
            "year": 2010,
        },
        {
            "name": "QCD Running",
            "title": "QCD and the Running Coupling Constant",
            "doi": "10.1016/j.physrep.2016.12.001",
            "year": 2017,
        },
    ],
}


def print_references():
    print("0.5 Nuclear Binding & Hadrons - References")
    for name, ref in REFERENCES["primary"].items():
        print(f"📚 {name}: DOI {ref['doi']}")


if __name__ == "__main__":
    print_references()
