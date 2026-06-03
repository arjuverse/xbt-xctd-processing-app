import streamlit as st

from modules.xbt import run_xbt
from modules.xctd import run_xctd

# ====================================================
# PAGE
# ====================================================

st.set_page_config(
    page_title="Ocean Profile Processing System",
    layout="wide"
)

st.title(
    "Ocean Profile Processing System"
)

st.info(
    """
Supports:

• XBT Processing

• XCTD Processing
"""
)

# ====================================================
# MODULE SELECT
# ====================================================

module = st.sidebar.radio(

    "Select Module",

    [

        "XBT",

        "XCTD"

    ]

)

# ====================================================
# LOAD MODULE
# ====================================================

if module == "XBT":

    run_xbt()

if module == "XCTD":

    run_xctd()
