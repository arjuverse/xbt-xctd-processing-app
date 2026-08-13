# 🌊 XBT/XCTD Processing System (MK-150 Based)

## Interactive Quality Control and Processing Platform for Expendable Ocean Profile Data

The **XBT/XCTD Processing System (MK-150 Based)** is a web-based scientific application designed for processing, quality control, visualization, correction, and interpolation of expendable oceanographic profile observations.

The application provides an interactive replacement for traditional command-line and shell-script based workflows by integrating the complete processing chain into an easy-to-use web interface.

---

## Supported Instruments

### 🌡 XBT - Expendable Bathythermograph

Processes ocean temperature profile observations.

Supported workflow:

- Raw XBT file upload
- EDF generation
- Temperature profile visualization
- Probe-to-probe consistency checking
- Interactive quality control editing
- Regenerated QC plots
- Vertical interpolation
- Final product export


### 🌊 XCTD - Expendable Conductivity Temperature Depth

Processes ocean temperature and salinity profile observations.

Supported workflow:

- Raw XCTD file upload
- EDF generation
- Temperature profile visualization
- Salinity profile visualization
- Temperature probe consistency check
- Salinity probe consistency check
- Interactive quality control editing
- Regenerated QC plots
- Vertical interpolation
- Final product export


---

# Processing Workflow


```text

Raw MK-150 Data ➡️ EDF Generation ➡️ Initial Quality Control ➡️ Interactive Manual Correction ➡️ Regenerated QC ➡️ 1 m / 5 m Interpolation ➡️ Final Results Download

```

---

# Main Features

## EDF Generation

Automatically converts raw instrument files into EDF formatted outputs.

Generated parameters:

### XBT

| Parameter |
|---|
| Depth |
| Temperature |
| Resistance |


### XCTD

| Parameter |
|---|
| Depth |
| Temperature |
| Salinity |
| Resistance |


---

## Interactive Quality Control

The system allows users to visually inspect profiles and manually correct:

- Temperature spikes
- Salinity spikes
- Spurious measurements
- Noisy tail sections
- Bottom impact errors


The corrected profile can be replotted immediately for verification.


---

## QC Visualization


### XBT

Generated plots:

- Temperature profile comparison
- Probe-to-probe consistency


### XCTD

Generated plots:

- Temperature profiles
- Salinity profiles
- Temperature probe-to-probe consistency
- Salinity probe-to-probe consistency


---

## Interpolation Products


After QC, users can generate:

### 1 metre interpolation

```text
Depth interval: 1 m
```

### 5 metre interpolation

```text
Depth interval: 5 m
```


Outputs:

- CSV formatted products
- Ready for further scientific analysis


---

# Repository Structure


```text
xbt-xctd-processing-app/


├── app.py


├── modules/

│   ├── xbt.py

│   └── xctd.py


├── sample_data/

│   ├── xbt/

│   └── xctd/


├── requirements.txt

├── README.md

└── LICENSE
```


---

# Installation


Clone the repository:


```bash
git clone https://github.com/arjuverse/xbt-xctd-processing-app.git

cd xbt-xctd-processing-app
```


Install dependencies:


```bash
pip install -r requirements.txt
```


Run application:


```bash
streamlit run app.py
```


---

# Required Python Packages


```text
streamlit
pandas
numpy
matplotlib
scipy
openpyxl
```


---

# Online Application


The web application can be accessed using the deployed Streamlit URL:


```text
https://xbt-xctd-mk150.streamlit.app/
```


---

# Sample Data


Example XBT and XCTD files are included for testing:


```text
sample_data/

├── xbt/

└── xctd/
```


Users can download the sample datasets directly from the application homepage.


---

# Outputs


The system generates:


## EDF Files

```text
xout_1.edf
xout_2.edf
...
```


## QC Figures

```text
Initial QC plots

Corrected QC plots
```


## Interpolated Data

```text
1m_interpolation.csv

5m_interpolation.csv
```


---

# Applications


This software is designed for:


- Ships of Oppurtunities and Oceanographic research cruises
- MK-150 Digital Converter by T.S.K
- XBT/XCTD data processing
- Temperature and Salinity data quality control


---

# Version


```text
Version: 2.0

Release: XBT/XCTD Processing System

Platform: Streamlit

Instrument workflow: MK-150 Based
```


---

# Developer


**Arjun K Sabu (arjunksabu@gmail.com)**

# Python Source Code

**Sidharth Sudheer (sidharthsudheer2000@gmail.com)**


XBT/XCTD Data Processing


---

# Citation


If you use this software in research, please cite:


```text
Arjun K Sabu (2026).

XBT/XCTD Processing System (MK-150 Based):

A Web-Based Quality Control and Processing Platform for Expendable Oceanographic Profile Data.

Version 2.0.
```


A DOI will be provided after Zenodo archival.


---

# License


This project is released for scientific and research use.

See LICENSE file for details.


---

# Acknowledgement


Developed to simplify and modernize expendable oceanographic profile processing workflows by replacing shell-script based processing with an interactive web-based platform.

