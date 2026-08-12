import pathlib

import xarray as xr
import copernicusmarine

datadir = pathlib.Path("data").absolute()
datadir.mkdir(exist_ok=True, parents=True)

vardict = {"salt":["cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m","so"],
           "temp":["cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m","thetao"]
}

def login(username, password):
    copernicusmarine.login(username=username, password=password)

def retrieve(data_var="salt"):
    copernicusmarine.subset(
        #dataset_id="cmems_mod_glo_phy_anfc_0.083deg_PT1H-m",
        #dataset_id="GLOBAL_ANALYSISFORECAST_PHY_001_024",
        #dataset_id="cmems_mod_glo_phy_anfc_0.083deg_P1D-m",
        dataset_id=vardict[data_var][0],
        variables=[vardict[data_var][1]],
        minimum_longitude=0,
        maximum_longitude=4,
        minimum_latitude=3,
        maximum_latitude=6,
        start_datetime="2025-08-08T00:00:00",
        end_datetime="2026-08-10T00:00:00",
        minimum_depth=0,
        maximum_depth=2000,
        file_format="netcdf",
        output_directory=datadir
    )

retrieve("salt")
retrieve("temp")
