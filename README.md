# GENERACION_Convert_BIDS

GENERACION_Convert_BIDS is a standardized MRI preprocessing and conversion pipeline adapted from MRIght, available [here](https://github.com/arnau-guell/mright). This version, adapted for the Generacion project, converts the raw DICOM images to BIDS format.

This pipeline allows you to go from raw DICOMs directly from the scanner to BIDS-compliant data, ready for preprocessing. It's designed to be used directly from the terminal. It works both in Linux and MacOS.

## Table of Contents

- [Step-by-Step Workflow](#step-by-step-workflow)
  - [Install the virtual environment](#install-the-virtual-environment)
  - [1. Convert to BIDS](#1-convert-to-bids)
- [License](#license)

---

## Step-by-Step Workflow

### Install the virtual environment

* 
    ```bash
    conda env create -f 0-env_config/environment.yml
    conda activate mright-env
    ```

---

### 1. Convert to BIDS

* 
    ```bash
    python 1-convert/DICOM_to_BIDS.py
    ```

    **Prompts for:** Path to DICOM directory, path to shared BIDS directory (for determining subjects who have already been processed), path to local (temporary) BIDS output directory, path to project heuristic file (i.e., `1-convert/heuristic_generacion.py`).

    **Output:** Creates a BIDS-compliant dataset in the specified temporary output directory.

---

## License 

GENERACION_Convert_BIDS © PENLab, University of Barcelona.  

Please cite appropriately if using this pipeline in publications.
