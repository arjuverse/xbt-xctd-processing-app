# =====================================================
# XBT MODULE WRAPPER
# =====================================================

import streamlit as st

def run_xctd():

    st.header("XCTD Processing")

    with st.expander(
        "📘 XCTD Processing Instructions",
        expanded=True
    ):

        st.markdown(
            """
## XCTD Quality Control Workflow

This module processes raw XCTD `.CTD` files and generates quality-controlled ocean profile products.

### Workflow

1. Upload raw `.CTD` files
2. Generate XCTD EDF files and initial QC plot
3. Inspect temperature and salinity profiles
4. Edit spike or spurious values in the EDF table
5. Regenerate the QC plot
6. Generate 1 m and 5 m interpolated outputs
7. Download final corrected products

### QC Editing

Use the editable table to:

- remove bad rows
- correct temperature spikes
- correct salinity spikes
- remove noisy tail values
- trim unreliable regions

### Final Outputs

- Corrected XCTD EDF ZIP
- Initial or corrected QC plot
- 1 m interpolated CSV
- 5 m interpolated CSV
"""
        )
def run_xbt():

    st.header(
        "XBT Processing"
    )

    st.info(
        """
Upload raw XBT files.

Workflow:

Generate EDF
→ QC
→ Edit
→ Regenerate
→ Interpolate
→ Download
"""
    )

    exec(
        open(
            "legacy_xbt.py",
            encoding="utf-8"
        ).read(),

        globals()
    )
