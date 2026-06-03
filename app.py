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
    page_title="Ocean Profile Processing System",
    layout="wide"
)


# =====================================================
# SAMPLE ZIP CREATOR
# =====================================================

def make_sample_zip(folder):

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
# TITLE
# =====================================================

st.title(
    "🌊 XBT/XCTD Processing System"
)

st.markdown(
    """
Interactive web-based processing platform for:

- Expendable Bathythermograph (XBT)
- Expendable Conductivity Temperature Depth (XCTD)

Processing workflow:

Raw data → EDF → QC → Editing → Interpolation → Final products
"""
)


# =====================================================
# STREAMLIT SLEEP NOTICE
# =====================================================

st.warning(
    """
If the app was inactive, loading may take 30–60 seconds while the server wakes up.
"""
)


# =====================================================
# SAMPLE DATA
# =====================================================

st.header(
    "Sample Data for Testing"
)


col1, col2 = st.columns(2)


with col1:

    if os.path.exists(
        "sample_data/xbt"
    ):

        st.download_button(

            "Download Sample XBT Data",

            make_sample_zip(
                "sample_data/xbt"
            ),

            "sample_xbt_data.zip",

            "application/zip"

        )


with col2:

    if os.path.exists(
        "sample_data/xctd"
    ):

        st.download_button(

            "Download Sample XCTD Data",

            make_sample_zip(
                "sample_data/xctd"
            ),

            "sample_xctd_data.zip",

            "application/zip"

        )


# =====================================================
# MODULE SELECTION
# =====================================================

st.sidebar.title(
    "Processing Module"
)


module = st.sidebar.radio(

    "Select Data Type",

    [

        "XBT",

        "XCTD"

    ]

)


# =====================================================
# RUN MODULES
# =====================================================

if module == "XBT":

    run_xbt()


elif module == "XCTD":

    run_xctd()
