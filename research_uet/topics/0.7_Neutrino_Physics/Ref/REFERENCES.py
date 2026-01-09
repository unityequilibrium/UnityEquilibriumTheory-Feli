"""
REFERENCES.py - 0.7 Neutrino Physics
=====================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "NuFIT": {
            "title": "Updated global analysis of neutrino oscillations",
            "authors": [
                "Esteban, I.",
                "Gonzalez-Garcia, M.C.",
                "Maltoni, M.",
                "Schwetz, T.",
                "Zhou, A.",
            ],
            "journal": "JHEP",
            "volume": "09",
            "pages": "178",
            "year": 2020,
            "doi": "10.1007/JHEP09(2020)178",
            "url": "http://www.nu-fit.org/",
        },
        "T2K": {
            "title": "Constraint on the matter-antimatter symmetry-violating phase in neutrino oscillations",
            "authors": ["T2K Collaboration"],
            "journal": "Nature",
            "volume": 580,
            "pages": "339",
            "year": 2020,
            "doi": "10.1038/s41586-020-2177-0",
        },
    },
    "supplementary": [
        {
            "name": "NOvA",
            "title": "First Measurement of Neutrino Oscillation Parameters using Neutrinos and Antineutrinos by NOvA",
            "doi": "10.1103/PhysRevLett.123.151803",
            "year": 2019,
        },
        {
            "name": "Super-K",
            "title": "Atmospheric neutrino oscillation analysis with external constraints",
            "doi": "10.1103/PhysRevD.97.072001",
            "year": 2018,
        },
    ],
}


def print_references():
    print("0.7 Neutrino Physics - References")
    for name, ref in REFERENCES["primary"].items():
        print(f"📚 {name}: DOI {ref['doi']}")


if __name__ == "__main__":
    print_references()
