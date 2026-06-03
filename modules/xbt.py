import streamlit as st


def run_xbt():

    st.header("XBT Processing")

    with st.expander(
        "📘 XBT Processing Instructions",
        expanded=True
    ):

        st.markdown(
            """
## XBT Quality Control Workflow

This module processes raw XBT `.XBT` files and generates quality-controlled ocean temperature profile products.

### Workflow

1. Upload raw `.XBT` files
2. Generate XBT EDF files and initial QC plot
3. Inspect temperature profiles and probe-to-probe consistency
4. Edit spike or spurious values in the EDF table
5. Regenerate the QC plot
6. Generate 1 m and 5 m interpolated outputs
7. Download final corrected products

### QC Editing

Use the editable table to:

- remove bad rows
- correct temperature spikes
- remove bottom-hit values
- remove noisy tail values
- trim unreliable regions

### Final Outputs

- Corrected XBT EDF ZIP
- Initial or corrected QC plot
- 1 m interpolated CSV
- 5 m interpolated CSV
"""
        )

    exec(
        open(
            "legacy_xbt.py",
            encoding="utf-8"
        ).read(),
        globals()
    )
