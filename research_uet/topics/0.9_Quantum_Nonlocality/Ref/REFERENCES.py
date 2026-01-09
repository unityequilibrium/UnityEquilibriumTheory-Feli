"""
REFERENCES.py - 0.9 Quantum Nonlocality
========================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "Bell_Original": {
            "title": "On the Einstein Podolsky Rosen paradox",
            "authors": ["Bell, J.S."],
            "journal": "Physics Physique Fizika",
            "volume": 1,
            "pages": "195",
            "year": 1964,
            "doi": "10.1103/PhysicsPhysiqueFizika.1.195",
        },
        "Aspect_1982": {
            "title": "Experimental Realization of Einstein-Podolsky-Rosen-Bohm Gedankenexperiment",
            "authors": ["Aspect, A.", "Grangier, P.", "Roger, G."],
            "journal": "Physical Review Letters",
            "volume": 49,
            "pages": "91",
            "year": 1982,
            "doi": "10.1103/PhysRevLett.49.91",
        },
    },
    "supplementary": [
        {
            "name": "Loophole-free",
            "title": "Loophole-free Bell inequality violation",
            "doi": "10.1038/nature15759",
            "year": 2015,
        }
    ],
}


def print_references():
    print("0.9 Quantum Nonlocality - References")
    for name, ref in REFERENCES["primary"].items():
        print(f"📚 {name}: DOI {ref['doi']}")


if __name__ == "__main__":
    print_references()
