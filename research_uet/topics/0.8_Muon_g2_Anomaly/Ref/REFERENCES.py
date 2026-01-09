"""
REFERENCES.py - 0.8 Muon g-2 Anomaly
=====================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "Fermilab_g2": {
            "title": "Measurement of the Positive Muon Anomalous Magnetic Moment to 0.46 ppm",
            "authors": ["Muon g-2 Collaboration"],
            "journal": "Physical Review Letters",
            "volume": 126,
            "pages": "141801",
            "year": 2021,
            "doi": "10.1103/PhysRevLett.126.141801",
        },
        "SM_Prediction": {
            "title": "The anomalous magnetic moment of the muon in the Standard Model",
            "authors": ["Aoyama, T.", "et al."],
            "journal": "Physics Reports",
            "volume": 887,
            "pages": "1-166",
            "year": 2020,
            "doi": "10.1016/j.physrep.2020.07.006",
        },
    },
    "supplementary": [
        {
            "name": "BNL E821",
            "title": "Final Report of the Muon E821 Anomalous Magnetic Moment Measurement at BNL",
            "doi": "10.1103/PhysRevD.73.072003",
            "year": 2006,
        }
    ],
}


def print_references():
    print("0.8 Muon g-2 Anomaly - References")
    for name, ref in REFERENCES["primary"].items():
        print(f"📚 {name}: DOI {ref['doi']}")


if __name__ == "__main__":
    print_references()
