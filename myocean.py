import pathlib

import xarray as xr

import copernicusmarine

datadir = pathlib.Path("data").absolute()
datadir.mkdir(exist_ok=True, parents=True)

def login(username, password):
    copernicusmarine.login(username=username, password=password)

def retrieve(variables=["uo"]):
    copernicusmarine.subset(
        dataset_id="cmems_mod_glo_phy_anfc_0.083deg_PT1H-m",
        variables=variables,
        minimum_longitude=-7.960792,
        maximum_longitude=11.087939,
        minimum_latitude=-5.457782,
        maximum_latitude=9.952427,
        start_datetime="2026-08-06T00:00:00",
        end_datetime="2026-08-06T00:00:00",
        minimum_depth=0.49402499198913574,
        maximum_depth=0.49402499198913574,
        file_format="zarr",
        output_directory=datadir
    )
