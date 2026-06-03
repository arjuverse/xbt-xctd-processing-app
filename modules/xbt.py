# =====================================================
# XBT MODULE WRAPPER
# =====================================================

import streamlit as st


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
