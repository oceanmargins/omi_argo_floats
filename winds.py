import pathlib

import pandas as pd
import cdsapi

AREA = [10,   # North
        -10,  # West
        -10,   # South
         10   # East
]
YEAR = "2026"

datadir = pathlib.Path("data").absolute()
datadir.mkdir(exist_ok=True, parents=True)
dataset = "reanalysis-era5-single-levels"

def download_era5(variable="10m_u_component_of_wind"):
    hours = ["00:00", "06:00", "12:00", "18:00"]  # 6 hourly
    out_file = datadir / f"{variable}_{YEAR}.grib"
    c = cdsapi.Client()
    print(f"Starting download: {variable}...")
    c.retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type": "reanalysis",
            "variable": variable,
            "year": YEAR,
            "month": [f"{m:02d}" for m in range(1, 13)],
            "day": [f"{d:02d}" for d in range(1, 32)],
            "time": hours,
            "area": AREA,
            "format": "grib"
        },
        out_file
    )
    print(f"Download completed: {out_file}")


def read_mettower():
    url = "https://uop.whoi.edu/currentprojects/Ghana/OMI_Tower.json"
    df = pd.read_json(url)
    df["time"] = pd.to_datetime(df.time)
    return df


def retrieve():
    download_era5("10m_u_component_of_wind", )
    download_era5("10m_v_component_of_wind", )
    df = read_mettower()
    df.to_hdf(datadir / "met_tower_data.h5")