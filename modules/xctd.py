import io
import zipfile

import pandas as pd
import streamlit as st

from modules.xctd_core import (
    generate_edf,
    generate_xctd_qc_plot,
    interpolate_xctd
)

def run_xctd():

    st.header("XCTD Processing")

    st.info(
        """
Upload raw `.CTD` files.

Workflow:

Generate XCTD EDF + Initial QC
→ Inspect temperature and salinity plots
→ Edit spike/spurious values in EDF table
→ Regenerate QC plot
→ Download corrected EDF ZIP and QC plot
"""
    )

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "xctd_edf_files" not in st.session_state:
        st.session_state["xctd_edf_files"] = []

    if "xctd_corrected_files" not in st.session_state:
        st.session_state["xctd_corrected_files"] = []

    if "xctd_initial_plot" not in st.session_state:
        st.session_state["xctd_initial_plot"] = None

    if "xctd_corrected_plot" not in st.session_state:
        st.session_state["xctd_corrected_plot"] = None

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

            st.error("Please upload XCTD files.")

        else:

            edf_files = generate_edf(
                uploaded_files,
                participants,
                start_date,
                end_date
            )

            st.session_state["xctd_edf_files"] = edf_files
            st.session_state["xctd_corrected_files"] = []
            st.session_state["xctd_corrected_plot"] = None

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

                st.session_state["xctd_initial_plot"] = (
                    plot_buffer.getvalue()
                )

                st.success(
                    f"Generated {len(edf_files)} XCTD EDF files."
                )

    # =====================================================
    # DISPLAY XCTD RESULTS
    # =====================================================

    edf_files = st.session_state["xctd_edf_files"]

    if edf_files:

        st.header("Initial XCTD QC Plot")

        fig = generate_xctd_qc_plot(
            edf_files
        )

        st.pyplot(fig)

        # =================================================
        # INTERACTIVE EDF QC EDITOR
        # =================================================

        st.header("Interactive XCTD EDF QC Editor")

        st.markdown(
            """
### Editing Instructions

- Remove spike rows
- Edit wrong temperature values
- Edit wrong salinity values
- Remove noisy tail values
- Click **Regenerate XCTD QC Plot** after editing
"""
        )

        corrected_files = []

        for item in edf_files:

            st.subheader(
                f"Edit {item['name']}"
            )

            edited_df = st.data_editor(
                item["df"],
                num_rows="dynamic",
                use_container_width=True,
                key=f"xctd_editor_{item['name']}"
            )

            edited_df["Depth"] = pd.to_numeric(
                edited_df["Depth"],
                errors="coerce"
            )

            edited_df["Temperature"] = pd.to_numeric(
                edited_df["Temperature"],
                errors="coerce"
            )

            edited_df["Salinity"] = pd.to_numeric(
                edited_df["Salinity"],
                errors="coerce"
            )

            edited_df["Resistance"] = pd.to_numeric(
                edited_df["Resistance"],
                errors="coerce"
            )

            edited_df = edited_df.dropna(
                subset=[
                    "Depth",
                    "Temperature",
                    "Salinity"
                ]
            )

            corrected_files.append(
                {
                    "name": item["name"],
                    "metadata": item["metadata"],
                    "df": edited_df
                }
            )

        # =================================================
        # REGENERATE QC
        # =================================================

        if st.button(
            "Regenerate XCTD QC Plot",
            key="regenerate_xctd_qc"
        ):

            st.session_state["xctd_corrected_files"] = (
                corrected_files
            )

            fig2 = generate_xctd_qc_plot(
                corrected_files
            )

            corrected_buffer = io.BytesIO()

            fig2.savefig(
                corrected_buffer,
                format="png",
                dpi=300,
                bbox_inches="tight"
            )

            st.session_state["xctd_corrected_plot"] = (
                corrected_buffer.getvalue()
            )

            st.success(
                "Corrected XCTD QC plot generated."
            )

        # =================================================
        # DISPLAY CORRECTED QC
        # =================================================

        if st.session_state["xctd_corrected_files"]:

            st.header("Corrected XCTD QC Plot")

            fig3 = generate_xctd_qc_plot(
                st.session_state["xctd_corrected_files"]
            )

            st.pyplot(fig3)

        # =================================================
        # FINAL FILE SELECTION
        # =================================================

        if st.session_state["xctd_corrected_files"]:
            final_files = st.session_state[
                "xctd_corrected_files"
            ]
        else:
            final_files = edf_files

        # =================================================
        # CREATE EDF ZIP
        # =================================================

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(
            zip_buffer,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zipf:

            for item in final_files:

                edf_text = make_xctd_edf_text_for_download(
                    item["metadata"],
                    item["df"]
                )

                zipf.writestr(
                    item["name"],
                    edf_text
                )
                
        
                # =================================================
        # XCTD INTERPOLATION
        # =================================================

        st.header(
            "XCTD Interpolation"
        )


        if st.button(
            "Generate XCTD 1m and 5m Interpolation"
        ):


            interp_1m = interpolate_xctd(

                final_files,

                1

            )


            interp_5m = interpolate_xctd(

                final_files,

                5

            )


            st.session_state[
                "xctd_interp_1m"
            ] = interp_1m


            st.session_state[
                "xctd_interp_5m"
            ] = interp_5m



        if "xctd_interp_1m" in st.session_state:


            st.subheader(
                "1 m XCTD Preview"
            )


            st.dataframe(

                st.session_state[
                    "xctd_interp_1m"
                ].head()

            )


            st.download_button(

                "Download XCTD 1m CSV",

                st.session_state[
                    "xctd_interp_1m"
                ].to_csv(
                    index=False
                ),

                "xctd_1m_interpolation.csv",

                "text/csv"

            )


        if "xctd_interp_5m" in st.session_state:


            st.subheader(
                "5 m XCTD Preview"
            )


            st.dataframe(

                st.session_state[
                    "xctd_interp_5m"
                ].head()

            )


            st.download_button(

                "Download XCTD 5m CSV",

                st.session_state[
                    "xctd_interp_5m"
                ].to_csv(
                    index=False
                ),

                "xctd_5m_interpolation.csv",

                "text/csv"

            )        

        # =================================================
        # DOWNLOADS
        # =================================================

        st.header("Downloads")

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                label="Download XCTD EDF ZIP",
                data=zip_buffer.getvalue(),
                file_name="xctd_edf_files.zip",
                mime="application/zip",
                key="download_xctd_edf_zip"
            )

        with col2:

            if st.session_state["xctd_corrected_plot"]:

                st.download_button(
                    label="Download Corrected XCTD QC Plot",
                    data=st.session_state["xctd_corrected_plot"],
                    file_name="xctd_corrected_qc_plot.png",
                    mime="image/png",
                    key="download_xctd_corrected_plot"
                )

            elif st.session_state["xctd_initial_plot"]:

                st.download_button(
                    label="Download Initial XCTD QC Plot",
                    data=st.session_state["xctd_initial_plot"],
                    file_name="xctd_initial_qc_plot.png",
                    mime="image/png",
                    key="download_xctd_initial_plot"
                )


def make_xctd_edf_text_for_download(metadata, df):

    metadata_text = (
        " // THIS IS AN MK-150 EXPORT DATA FILE (EDF)\n"
    )

    for key, value in metadata.items():

        metadata_text += f"{key}: {value}\n"

    metadata_text += "\n"

    data_text = df.to_csv(
        sep="\t",
        index=False,
        float_format="%.3f"
    )

    return metadata_text + data_text
