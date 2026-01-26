"""
UET Cancer Research: Biomarker Identification System
====================================================
Topic: 0.22 Biophysics & Origin of Life
Goal: Identify specific genes (Biomarkers) that show early 'Information Decay'.

UET Principle:
"Biomarkers are high-utility nodes (Ω') that exhibit anomalous entropy spikes
before the macroscopic biological system (Ω) collapses."
"""

import numpy as np
import pandas as pd


def identify_biomarkers():
    print("🎯 UET BIOMARKER IDENTIFICATION: SEARCHING FOR CRITICAL NODES")
    print("=" * 60)

    # 1. Dataset Simulation (Focusing on a subset of 50 genes)
    gene_names = [f"GENE_{i:03d}" for i in range(50)]
    samples = 100

    # Mocking Gene Expression Data with some 'Anomalous' genes
    data = np.random.normal(5, 0.5, (50, samples))

    # Injecting anomalous entropy into Gene_007 and Gene_023 (Potential Biomarkers)
    data[7] = np.random.normal(5, 2.5, samples)
    data[23] = np.random.normal(5, 3.0, samples)

    print(f"Analyzing {len(gene_names)} candidate genes across {samples} samples...")

    # 2. UET Entropy Grading (The Identification Engine)
    results = []
    threshold = 0.5  # Entropy threshold for a Biomarker

    for i in range(len(gene_names)):
        variance = np.var(data[i])
        # UET Stability Grade (1.0 = Perfect Unity, 0.0 = Pure Chaos)
        stability = 1.0 / (1.0 + variance)

        if stability < threshold:
            results.append(
                {
                    "Gene": gene_names[i],
                    "Stability": stability,
                    "Status": "🚨 HIGH RISK (Potential Biomarker)",
                }
            )

    # 3. Output Findings
    print("\n[Analysis Report]")
    if results:
        df_results = pd.DataFrame(results)
        print(df_results.to_string(index=False))
    else:
        print("No significant biomarkers detected within current parameters.")

    print("\n[UET Clinical Insight]")
    print(
        "Genes with low stability are 'Information Leaks' that weaken the cellular field."
    )
    print("Targeting these nodes early can stabilize the global Information Balance.")

    return True


if __name__ == "__main__":
    identify_biomarkers()
