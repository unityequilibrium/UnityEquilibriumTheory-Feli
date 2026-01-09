"""
REFERENCES.py - 0.11 Phase Transitions
=======================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "BEC_Cornell_Wieman": {
            "title": "Observation of Bose-Einstein Condensation in a Dilute Atomic Vapor",
            "authors": [
                "Anderson, M.H.",
                "Ensher, J.R.",
                "Matthews, M.R.",
                "Wieman, C.E.",
                "Cornell, E.A.",
            ],
            "journal": "Science",
            "volume": 269,
            "pages": "198",
            "year": 1995,
            "doi": "10.1126/science.269.5221.198",
        },
        "Ising_Model": {
            "title": "Crystal Statistics. I. A Two-Dimensional Model with an Order-Disorder Transition",
            "authors": ["Onsager, L."],
            "journal": "Physical Review",
            "volume": 65,
            "pages": "117",
            "year": 1944,
            "doi": "10.1103/PhysRev.65.117",
        },
    }
}


def print_references():
    print("0.11 Phase Transitions - References")
    for name, ref in REFERENCES["primary"].items():
        print(f"📚 {name}: DOI {ref['doi']}")


if __name__ == "__main__":
    print_references()
