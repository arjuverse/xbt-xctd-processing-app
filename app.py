import streamlit as st

import os
import io
import zipfile

from modules.xbt import run_xbt
from modules.xctd import run_xctd


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="XBT/XCTD Processing System (MK-150 Based)",
    page_icon="🌊",
    layout="wide"
)


# =====================================================
# SAMPLE ZIP FUNCTION
# =====================================================

def create_zip(folder):

    buffer = io.BytesIO()

    with zipfile.ZipFile(
        buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for root, dirs, files in os.walk(folder):

            for file in files:

                path = os.path.join(
                    root,
                    file
                )

                zipf.write(
                    path,
                    arcname=file
                )

    return buffer.getvalue()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title(
    "🌊 XBT/XCTD System"
)

module = st.sidebar.radio(
    "Select Processing Module",
    [
        "Home",
        "XBT Processing",
        "XCTD Processing"
    ]
)


# =====================================================
# HOME PAGE
# =====================================================

if module == "Home":

    st.title(
        "🌊 XBT/XCTD Processing System (MK-150 Based)"
    )

    st.subheader(
        "Interactive Quality Control and Interpolation Platform"
    )

    st.markdown(
        """
A web-based scientific application for processing expendable oceanographic
profile observations generated from MK-150 based workflows.

Supported instruments:

### 🌡 XBT — Expendable Bathythermograph

Processes temperature profiles.

### 🌊 XCTD — Expendable Conductivity Temperature Depth

Processes temperature and salinity profiles.

---

## Processing Pipeline

Raw MK-150 Data ➡️ EDF Generation ➡️ Initial Quality Control ➡️ Interactive Manual Correction ➡️ Regenerated QC ➡️ 1 m / 5 m Interpolation ➡️ Final Results Download

---
"""
    )

    

    # =================================================
    # SAMPLE SYNTHETIC DATA
    # =================================================

    st.header(
        "📦 Sample Synthetic Data"
    )

    st.info(
        """
New users can download sample files below
and test the complete processing workflow.
"""
    )

    col1, col2 = st.columns(2)

    with col1:

        if os.path.exists(
            "sample_data/xbt"
        ):

            st.download_button(
                "Download Sample XBT Data",
                create_zip(
                    "sample_data/xbt"
                ),
                "sample_xbt_data.zip",
                "application/zip"
            )

        else:

            st.warning(
                "Sample XBT folder not found."
            )

    with col2:

        if os.path.exists(
            "sample_data/xctd"
        ):

            st.download_button(
                "Download Sample XCTD Data",
                create_zip(
                    "sample_data/xctd"
                ),
                "sample_xctd_data.zip",
                "application/zip"
            )

        else:

            st.warning(
                "Sample XCTD folder not found."
            )

    st.warning(
        """
If the app was inactive,
Streamlit Cloud may take 30–60 seconds to wake up.
"""
    )

# =================================================
# ABOUT
# =================================================

    st.header("About")

    st.markdown(
        """
**Version:** v2.0  

**System:** MK-150 Based  

**Modules:**  
- XBT Processing  
- XCTD Processing  

**Developer:** Arjun K Sabu (arjunksabu@gmail.com)

**Python Source Code:** Sidharth Sudheer (sidharthsudheer2000@gmail.com)
"""
    )

# =====================================================
# XBT MODULE
# =====================================================

elif module == "XBT Processing":

    run_xbt()


# =====================================================
# XCTD MODULE
# =====================================================

elif module == "XCTD Processing":

    run_xctd()