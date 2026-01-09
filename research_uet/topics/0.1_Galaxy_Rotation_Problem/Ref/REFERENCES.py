"""
REFERENCES.py - 0.1 Galaxy Rotation Problem
============================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "SPARC": {
            "title": "Spitzer Photometry and Accurate Rotation Curves (SPARC)",
            "authors": ["Lelli, F.", "McGaugh, S.S.", "Schombert, J.M."],
            "journal": "Astronomical Journal",
            "volume": 152,
            "pages": 157,
            "year": 2016,
            "doi": "10.3847/0004-6256/152/6/157",
            "url": "http://astroweb.cwru.edu/SPARC/",
        },
        "McGaugh_RAR": {
            "title": "Radial Acceleration Relation in Rotationally Supported Galaxies",
            "authors": ["McGaugh, S.S.", "Lelli, F.", "Schombert, J.M."],
            "journal": "Physical Review Letters",
            "volume": 117,
            "pages": "201101",
            "year": 2016,
            "doi": "10.1103/PhysRevLett.117.201101",
        },
    },
    "supplementary": [
        {
            "name": "LITTLE THINGS",
            "title": "Local Irregulars That Trace Luminosity Extremes, The H I Nearby Galaxy Survey",
            "doi": "10.3847/1538-3881/153/1/6",
            "year": 2017,
        },
        {
            "name": "THINGS",
            "title": "The H I Nearby Galaxy Survey",
            "doi": "10.1088/0004-6256/136/6/2563",
            "year": 2008,
        },
    ],
}


def print_references():
    """Print all references with DOIs."""
    print("=" * 60)
    print("0.1 Galaxy Rotation Problem - References")
    print("=" * 60)
    for name, ref in REFERENCES["primary"].items():
        print(f"\n📚 {name}")
        print(f"   Title: {ref['title']}")
        print(f"   DOI: {ref['doi']}")


if __name__ == "__main__":
    print_references()
