"""
REFERENCES.py - 0.4 Superconductivity & Superfluids
====================================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "CODATA_2018": {
            "title": "CODATA Recommended Values of the Fundamental Physical Constants: 2018",
            "authors": ["Tiesinga, E.", "Mohr, P.J.", "Newell, D.B.", "Taylor, B.N."],
            "journal": "Reviews of Modern Physics",
            "volume": 93,
            "pages": "025010",
            "year": 2021,
            "doi": "10.1103/RevModPhys.93.025010",
        },
        "BCS_Theory": {
            "title": "Theory of Superconductivity",
            "authors": ["Bardeen, J.", "Cooper, L.N.", "Schrieffer, J.R."],
            "journal": "Physical Review",
            "volume": 108,
            "pages": 1175,
            "year": 1957,
            "doi": "10.1103/PhysRev.108.1175",
        },
    },
    "supplementary": [
        {
            "name": "Helium-4",
            "title": "Properties of Liquid Helium",
            "doi": "10.1103/RevModPhys.29.205",
            "year": 1957,
        }
    ],
}


def print_references():
    print("0.4 Superconductivity & Superfluids - References")
    for name, ref in REFERENCES["primary"].items():
        print(f"📚 {name}: DOI {ref['doi']}")


if __name__ == "__main__":
    print_references()
