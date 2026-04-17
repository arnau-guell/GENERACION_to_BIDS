# GENERACION_to_BIDS

GENERACION_to_BIDS is a standardized MRI preprocessing and conversion pipeline adapted from MRIght, available [here](https://github.com/arnau-guell/mright). This version, adapted for the Generacion project, converts the raw DICOM images to BIDS format.

This pipeline allows you to go from raw DICOMs directly from the scanner to BIDS-compliant data, ready for preprocessing. It's designed to be used directly from the terminal. It works both in Linux and MacOS.

## Table of Contents

- [Step-by-Step Workflow](#step-by-step-workflow)
  - [Install the virtual environment](#0-install-the-virtual-environment)
  - [1. Copy DICOM files from the hard disk to the workstation](#1-copy-dicom-files-from-the-hard-disk-to-the-workstation)
  - [2. Convert to BIDS](#2-convert-to-bids)
- [License](#license)

---

## Step-by-Step Workflow

### 0. Install the virtual environment

* 
    ```bash
    conda env create -f scripts/00_environment.yml
    conda activate generacion-to-bids
    ```

---

### 1. Copy DICOM files from the hard disk to the workstation

* 
    ```bash
    python scripts/01_copy_dicoms_from_disk.py
    ```

---

### 2. Convert to BIDS

* 
    ```bash
    python scripts/02_DICOM_to_BIDS.py
    ```

    **Prompts for:** Path to DICOM directory, path to shared BIDS directory (for determining subjects who have already been processed), path to local (temporary) BIDS output directory, path to project heuristic file (i.e., `scripts/02b_heuristic_generacion.py`).

    **Output:** Creates a BIDS-compliant dataset in the specified temporary output directory.

* 
    ```bash
    python scripts/03_move_and_merge.py
    ```

    **Prompts for:** Path to temporary BIDS output directory, path to shared BIDS destination directory.

    **Output:** Moves the BIDS compliant data from a temporary directory to a shared destination directory.

---

## License 

GENERACION_to_BIDS © PENLab, University of Barcelona.  

Please cite appropriately if using this pipeline in publications.
