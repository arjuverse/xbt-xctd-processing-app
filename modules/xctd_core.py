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
