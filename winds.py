import pathlib
import os
os.environ["SSL_CERT_FILE"] = "/Users/bror/projects/obvi/omi_argo_floats/.certs/cacert_plus_incommon.pem"

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
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "sea_surface_temperature"
    ],
    "year": ["2026"],
    "month": ["01", "02", "03", "04", "05", "06","07"],
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ],
    "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [10, -10, -10, 10]
}


def download_era5(variable):
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