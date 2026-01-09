"""
REFERENCES.py - 0.3 Cosmology & Hubble Tension
===============================================
DOIs for all data sources used in this topic.
"""

REFERENCES = {
    "primary": {
        "Planck_2018": {
            "title": "Planck 2018 Results. VI. Cosmological Parameters",
            "authors": ["Planck Collaboration"],
            "journal": "Astronomy & Astrophysics",
            "volume": 641,
            "pages": "A6",
            "year": 2020,
            "doi": "10.1051/0004-6361/201833910",
        },
        "SH0ES_2022": {
            "title": "A Comprehensive Measurement of the Local Value of the Hubble Constant",
            "authors": ["Riess, A.G.", "et al."],
            "journal": "Astrophysical Journal Letters",
            "volume": 934,
            "pages": "L7",
            "year": 2022,
            "doi": "10.3847/2041-8213/ac5c5b",
        },
    },
    "supplementary": [
        {
            "name": "BOSS BAO",
            "title": "The clustering of galaxies in the completed SDSS-III",
            "doi": "10.1093/mnras/stx721",
            "year": 2017,
        },
        {
            "name": "JWST Early",
            "title": "JWST Early Release Science",
            "doi": "10.3847/2041-8213/aca086",
            "year": 2022,
        },
    ],
}


def print_references():
    print("=" * 60)
    print("0.3 Cosmology & Hubble Tension - References")
    print("=" * 60)
    for name, ref in REFERENCES["primary"].items():
        print(f"\n📚 {name}")
        print(f"   DOI: {ref['doi']}")


if __name__ == "__main__":
    print_references()
