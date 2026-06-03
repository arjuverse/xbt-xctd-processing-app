import io
import zipfile

import streamlit as st

from modules.xctd_core import generate_edf


def run_xctd():

    st.header("XCTD Processing")

    st.info(
        """
Upload raw `.CTD` files.

Current stage:
Generate XCTD EDF files, preview them, and download EDF ZIP.
"""
    )

    st.sidebar.header("XCTD Cruise Information")

    participants = st.sidebar.text_input(
        "XCTD Participants",
        key="xctd_participants"
    )

    start_date = st.sidebar.text_input(
        "XCTD Start Date",
        key="xctd_start_date"
    )

    end_date = st.sidebar.text_input(
        "XCTD End Date",
        key="xctd_end_date"
    )

    uploaded_files = st.file_uploader(
        "Upload XCTD `.CTD` Files",
        type=["ctd", "CTD"],
        accept_multiple_files=True,
        key="xctd_upload"
    )

    if st.button(
        "Generate XCTD EDF",
        key="generate_xctd_edf"
    ):

        if not uploaded_files:

            st.error("Please upload XCTD files.")

        else:

            edf_files = generate_edf(
                uploaded_files,
                participants,
                start_date,
                end_date
            )

            st.session_state["xctd_edf_files"] = edf_files

    if "xctd_edf_files" in st.session_state:

        edf_files = st.session_state["xctd_edf_files"]

        if not edf_files:

            st.error(
                "No EDF files generated. Please check the CTD file format."
            )

        else:

            st.success(
                f"Generated {len(edf_files)} XCTD EDF files."
            )

            for item in edf_files:

                st.subheader(item["name"])

                st.dataframe(
                    item["df"].head()
                )

            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(
                zip_buffer,
                "w",
                zipfile.ZIP_DEFLATED
            ) as zipf:

                for item in edf_files:

                    zipf.writestr(
                        item["name"],
                        item["edf_text"]
                    )

            st.download_button(
                label="Download XCTD EDF ZIP",
                data=zip_buffer.getvalue(),
                file_name="xctd_edf_files.zip",
                mime="application/zip",
                key="download_xctd_edf_zip"
            )
