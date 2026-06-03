import io
import zipfile

import streamlit as st

from modules.xctd_core import (
    generate_edf,
    generate_xctd_qc_plot
)


def run_xctd():

    st.header("XCTD Processing")

    st.info(
        """
Upload raw `.CTD` files.

Current workflow:

Generate XCTD EDF
→ Initial QC Plot
→ Preview EDF Data
→ Download EDF ZIP
"""
    )

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "xctd_edf_files" not in st.session_state:

        st.session_state["xctd_edf_files"] = []

    if "xctd_initial_plot" not in st.session_state:

        st.session_state["xctd_initial_plot"] = None

    # =====================================================
    # XCTD CRUISE INFORMATION
    # =====================================================

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

    # =====================================================
    # FILE UPLOAD
    # =====================================================

    uploaded_files = st.file_uploader(
        "Upload XCTD `.CTD` Files",
        type=["ctd", "CTD"],
        accept_multiple_files=True,
        key="xctd_upload"
    )

    # =====================================================
    # GENERATE EDF + INITIAL QC
    # =====================================================

    if st.button(
        "Generate XCTD EDF + Initial QC",
        key="generate_xctd_edf_qc"
    ):

        if not uploaded_files:

            st.error(
                "Please upload XCTD files."
            )

        else:

            edf_files = generate_edf(
                uploaded_files,
                participants,
                start_date,
                end_date
            )

            st.session_state[
                "xctd_edf_files"
            ] = edf_files

            if not edf_files:

                st.error(
                    "No EDF files generated. Please check the CTD file format."
                )

            else:

                fig = generate_xctd_qc_plot(
                    edf_files
                )

                plot_buffer = io.BytesIO()

                fig.savefig(
                    plot_buffer,
                    format="png",
                    dpi=300,
                    bbox_inches="tight"
                )

                st.session_state[
                    "xctd_initial_plot"
                ] = plot_buffer.getvalue()

                st.success(
                    f"Generated {len(edf_files)} XCTD EDF files."
                )

    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    edf_files = st.session_state[
        "xctd_edf_files"
    ]

    if edf_files:

        st.header(
            "Initial XCTD QC Plot"
        )

        fig = generate_xctd_qc_plot(
            edf_files
        )

        st.pyplot(
            fig
        )

        # =================================================
        # EDF PREVIEW
        # =================================================

        st.header(
            "XCTD EDF Preview"
        )

        for item in edf_files:

            st.subheader(
                item["name"]
            )

            st.dataframe(
                item["df"].head()
            )

        # =================================================
        # EDF ZIP DOWNLOAD
        # =================================================

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

        st.header(
            "Downloads"
        )

        st.download_button(
            label="Download XCTD EDF ZIP",
            data=zip_buffer.getvalue(),
            file_name="xctd_edf_files.zip",
            mime="application/zip",
            key="download_xctd_edf_zip"
        )

        if st.session_state[
            "xctd_initial_plot"
        ] is not None:

            st.download_button(
                label="Download XCTD Initial QC Plot",
                data=st.session_state[
                    "xctd_initial_plot"
                ],
                file_name="xctd_initial_qc_plot.png",
                mime="image/png",
                key="download_xctd_initial_plot"
            )
