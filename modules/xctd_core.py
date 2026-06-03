import io
from datetime import datetime

import pandas as pd


def corrector_xctd(df):

    df = df.dropna(
        subset=["Depth", "Temperature", "Salinity"]
    )

    if df.empty:
        return df

    closest_depth_idx = (
        df["Depth"] - 5
    ).abs().idxmin()

    temp_at_5m = df.loc[
        closest_depth_idx,
        "Temperature"
    ]

    sal_at_5m = df.loc[
        closest_depth_idx,
        "Salinity"
    ]

    df.loc[
        df["Depth"] < 5,
        "Temperature"
    ] = temp_at_5m

    df.loc[
        df["Depth"] < 5,
        "Salinity"
    ] = sal_at_5m

    return df


def create_metadata(first_line, participants, start_date, end_date):

    metadata = first_line.split(",")

    return {
        "Date of Launch":
            datetime.strptime(
                metadata[2].strip(),
                "%Y%m%d"
            ).strftime("%m/%d/%Y"),

        "Time of Launch":
            datetime.strptime(
                metadata[3].strip(),
                "%H%M%S"
            ).strftime("%H:%M:%S"),

        "Sequence #": metadata[1].strip(),

        "Latitude": metadata[4].strip(),

        "Longitude": metadata[5].strip(),

        "Probe type": metadata[6].strip(),

        "Transect route dated from":
            f"{start_date} to {end_date}",

        "Participants are": participants
    }


def make_edf_text(metadata, df):

    text = " // THIS IS AN MK-150 EXPORT DATA FILE (EDF)\n"

    for key, value in metadata.items():
        text += f"{key}: {value}\n"

    text += "\n"

    text += df.to_csv(
        sep="\t",
        index=False,
        float_format="%.3f"
    )

    return text


def generate_edf(uploaded_files, participants, start_date, end_date):

    edf_files = []

    for idx, uploaded_file in enumerate(uploaded_files, start=1):

        raw = uploaded_file.getvalue()

        decoded = raw.decode(
            "utf-8",
            errors="ignore"
        )

        lines = decoded.splitlines()

        if not lines:
            continue

        first_line = lines[0]

        metadata = create_metadata(
            first_line,
            participants,
            start_date,
            end_date
        )

        df_raw = pd.read_csv(
            io.StringIO(decoded),
            skiprows=1,
            header=None,
            sep=",",
            names=[
                "Depth",
                "Temperature",
                "Conductivity",
                "Salinity",
                "SoundVelocity",
                "Density",
                "Blank"
            ],
            engine="python"
        )

        df = df_raw[
            [
                "Depth",
                "Temperature",
                "Salinity"
            ]
        ].copy()

        df["Depth"] = pd.to_numeric(
            df["Depth"],
            errors="coerce"
        )

        df["Temperature"] = pd.to_numeric(
            df["Temperature"],
            errors="coerce"
        )

        df["Salinity"] = pd.to_numeric(
            df["Salinity"],
            errors="coerce"
        )

        df = df.dropna(
            subset=[
                "Depth",
                "Temperature",
                "Salinity"
            ]
        )

        if df.empty:
            continue

        df["Depth"] = df["Depth"].round(1)

        df = corrector_xctd(df)

        df["Resistance"] = 9999.99

        name = f"xout_{idx}.edf"

        edf_text = make_edf_text(
            metadata,
            df
        )

        edf_files.append(
            {
                "name": name,
                "metadata": metadata,
                "df": df,
                "edf_text": edf_text
            }
        )

    return edf_files
    
# ==================================================
# XCTD QC PLOT
# ==================================================

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



def generate_xctd_qc_plot(edf_files):

    fig = plt.figure(figsize=(16, 14))

    gs = gridspec.GridSpec(
        2,
        3,
        width_ratios=[2.5, 2.5, 1],
        height_ratios=[1, 1],
        hspace=0.22,
        wspace=0.18
    )

    ax1 = fig.add_subplot(gs[0, 0])  # Temp offset
    ax2 = fig.add_subplot(gs[1, 0])  # Sal offset
    ax3 = fig.add_subplot(gs[0, 1])  # Temp consistency
    ax4 = fig.add_subplot(gs[1, 1])  # Sal consistency
    ax5 = fig.add_subplot(gs[:, 2])  # Legend

    increm = 0
    offset = 3

    lines = []
    labels = []

    for item in edf_files:

        df = item["df"]

        line, = ax1.plot(
            df["Temperature"] + increm,
            df["Depth"],
            linewidth=1.5
        )

        ax2.plot(
            df["Salinity"] + increm,
            df["Depth"],
            linewidth=1.5
        )

        ax3.plot(
            df["Temperature"],
            df["Depth"],
            linewidth=1.5
        )

        ax4.plot(
            df["Salinity"],
            df["Depth"],
            linewidth=1.5
        )

        lines.append(line)
        labels.append(item["name"])

        increm += offset

    for ax in [ax1, ax2, ax3, ax4]:
        ax.invert_yaxis()
        ax.grid(True, linestyle="--", alpha=0.2)
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

    ax1.set_title("Temperature Profiles")
    ax1.set_xlabel("Temperature (°C) + Offset")
    ax1.set_ylabel("Depth (m)")

    ax2.set_title("Salinity Profiles")
    ax2.set_xlabel("Salinity (PSU) + Offset")
    ax2.set_ylabel("Depth (m)")

    ax3.set_title("Temperature Probe-to-Probe Consistency")
    ax3.set_xlabel("Temperature (°C)")
    ax3.set_ylabel("Depth (m)")

    ax4.set_title("Salinity Probe-to-Probe Consistency")
    ax4.set_xlabel("Salinity (PSU)")
    ax4.set_ylabel("Depth (m)")

    ax5.axis("off")
    ax5.legend(
        lines,
        labels,
        fontsize=10,
        frameon=True,
        loc="center"
    )

    return fig
    
# ==================================================
# XCTD INTERPOLATION
# ==================================================

from scipy.interpolate import interp1d
import numpy as np


def interpolate_xctd(
    edf_files,
    interval
):

    output_rows = []

    for item in edf_files:

        df = item["df"].copy()

        df = df.dropna(
            subset=[
                "Depth",
                "Temperature",
                "Salinity"
            ]
        )

        df = df.sort_values(
            "Depth"
        )

        max_depth = int(
            df["Depth"].max()
        )


        new_depth = np.arange(
            0,
            max_depth + interval,
            interval
        )


        temp_interp = interp1d(
            df["Depth"],
            df["Temperature"],
            bounds_error=False,
            fill_value=np.nan
        )


        sal_interp = interp1d(
            df["Depth"],
            df["Salinity"],
            bounds_error=False,
            fill_value=np.nan
        )


        row = {
            "Profile":
            item["name"]
        }


        for d, t in zip(
            new_depth,
            temp_interp(new_depth)
        ):

            row[
                f"Temp_{int(d)}"
            ] = round(
                float(t),
                3
            )


        for d, s in zip(
            new_depth,
            sal_interp(new_depth)
        ):

            row[
                f"Sal_{int(d)}"
            ] = round(
                float(s),
                3
            )


        output_rows.append(
            row
        )


    return pd.DataFrame(
        output_rows
    )
