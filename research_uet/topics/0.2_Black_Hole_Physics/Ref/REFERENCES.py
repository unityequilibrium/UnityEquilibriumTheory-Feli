"""
REFERENCES.py - 0.2 Black Hole Physics
=======================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "EHT_M87": {
            "title": "First M87 Event Horizon Telescope Results. I. The Shadow of the Supermassive Black Hole",
            "authors": ["Event Horizon Telescope Collaboration"],
            "journal": "Astrophysical Journal Letters",
            "volume": 875,
            "pages": "L1",
            "year": 2019,
            "doi": "10.3847/2041-8213/ab0ec7",
        },
        "LIGO_GW150914": {
            "title": "Observation of Gravitational Waves from a Binary Black Hole Merger",
            "authors": ["Abbott, B.P.", "et al.", "LIGO Scientific Collaboration"],
            "journal": "Physical Review Letters",
            "volume": 116,
            "pages": "061102",
            "year": 2016,
            "doi": "10.1103/PhysRevLett.116.061102",
        },
    },
    "supplementary": [
        {
            "name": "Sgr A*",
            "title": "First Sagittarius A* Event Horizon Telescope Results",
            "doi": "10.3847/2041-8213/ac6674",
            "year": 2022,
        },
        {
            "name": "CCBH Farrah",
            "title": "Observational Evidence for Cosmological Coupling of Black Holes",
            "doi": "10.3847/2041-8213/acb704",
            "year": 2023,
        },
    ],
}


def print_references():
    print("=" * 60)
    print("0.2 Black Hole Physics - References")
    print("=" * 60)
    for name, ref in REFERENCES["primary"].items():
        print(f"\n📚 {name}")
        print(f"   DOI: {ref['doi']}")


if __name__ == "__main__":
    print_references()
