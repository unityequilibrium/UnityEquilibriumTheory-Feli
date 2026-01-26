# 📊 Real Data Source: Seizure Prediction

## CHB-MIT Scalp EEG Database

### Access Information

| Field | Value |
|:------|:------|
| **URL** | https://physionet.org/content/chbmit/1.0.0/ |
| **Size** | ~21 GB |
| **Format** | EDF (European Data Format) |
| **License** | Open Database License (ODbL) |

### Download Script

```python
#!/usr/bin/env python
"""
Download CHB-MIT EEG data from PhysioNet.

Usage:
    python download_chbmit.py --subjects 1,2,3 --output data/
"""

import os
import urllib.request
from pathlib import Path

BASE_URL = "https://physionet.org/files/chbmit/1.0.0/"

def download_subject(subject_id: int, output_dir: str = "data"):
    """Download EEG files for one subject."""
    output = Path(output_dir) / f"chb{subject_id:02d}"
    output.mkdir(parents=True, exist_ok=True)
    
    # Download summary file
    summary_url = f"{BASE_URL}chb{subject_id:02d}/chb{subject_id:02d}-summary.txt"
    summary_path = output / f"chb{subject_id:02d}-summary.txt"
    
    print(f"Downloading summary for chb{subject_id:02d}...")
    urllib.request.urlretrieve(summary_url, summary_path)
    
    print(f"✅ Downloaded to {output}")
    return output

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--subjects", default="1", help="Comma-separated subject IDs")
    parser.add_argument("--output", default="data", help="Output directory")
    args = parser.parse_args()
    
    subjects = [int(s) for s in args.subjects.split(",")]
    for subj in subjects:
        download_subject(subj, args.output)
```

### Quick Access (Subset)

For testing, use pre-processed subset:

```bash
# Download sample seizure recording (smaller file)
wget https://physionet.org/files/chbmit/1.0.0/chb01/chb01_03.edf
```

### File Format

EDF files contain:
- 23 EEG channels at 256 Hz
- Continuous recording
- Seizure annotations in summary.txt

### Seizure Annotations

From `chb01-summary.txt`:
```
File Name: chb01_03.edf
Number of Seizures in File: 1
Seizure Start Time: 2996 seconds
Seizure End Time: 3036 seconds
```

---

## How to Load Data

```python
import mne

# Load EDF file
raw = mne.io.read_raw_edf("chb01_03.edf", preload=True)

# Get data
data = raw.get_data()  # (n_channels, n_samples)
sfreq = raw.info['sfreq']  # 256 Hz

print(f"Shape: {data.shape}")
print(f"Sampling rate: {sfreq} Hz")
```

---

*"Real data from real patients — not simulations."*
