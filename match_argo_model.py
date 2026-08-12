import pathlib

import numpy as np
import pandas as pd
import xarray as xr
from scipy.spatial import cKDTree

DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data"
ARGO_FILE = DATA_DIR / "argo_data.h5"


def _latest_match(pattern):
    matches = sorted(DATA_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No file matching {pattern!r} in {DATA_DIR}")
    return matches[-1]


def _nearest_1d(grid, values):
    """Index into a sorted 1-D grid nearest each value."""
    idx = np.searchsorted(grid, values)
    idx = np.clip(idx, 1, len(grid) - 1)
    left, right = grid[idx - 1], grid[idx]
    idx -= (values - left) < (right - values)
    return idx


def match_argo_to_model(argo_file=ARGO_FILE, temp_file=None, salt_file=None):
    """Match each Argo profile point to its nearest CMEMS model grid cell.

    Adds "model_temp" and "model_salt" columns to the Argo dataframe, taken
    from the CMEMS thetao/so netcdf files at the model grid cell nearest to
    each Argo (time, pres, latitude, longitude) observation.

    Horizontal matching (latitude/longitude) uses a scipy cKDTree over the
    model's lat/lon grid. Time and depth are matched separately with a
    nearest-value search, since a single KDTree across lat/lon/depth/time
    would mix incompatible units (degrees, meters, nanoseconds) into one
    Euclidean distance.
    """
    temp_file = temp_file or _latest_match("*phy-thetao_*.nc")
    salt_file = salt_file or _latest_match("*phy-so_*.nc")

    df = pd.read_hdf(argo_file, key="df").reset_index(drop=True)

    ds = xr.open_dataset(temp_file)
    ds["so"] = xr.open_dataset(salt_file)["so"]

    lat = ds.latitude.values
    lon = ds.longitude.values
    depth = ds.depth.values
    time = ds.time.values

    lon_grid, lat_grid = np.meshgrid(lon, lat)
    tree = cKDTree(np.column_stack([lat_grid.ravel(), lon_grid.ravel()]))
    _, flat_idx = tree.query(np.column_stack([df.latitude.values, df.longitude.values]))
    lat_idx, lon_idx = np.unravel_index(flat_idx, lat_grid.shape)

    argo_time = df.time.dt.tz_localize(None).values.astype(time.dtype)
    time_idx = _nearest_1d(time, argo_time)
    depth_idx = _nearest_1d(depth, df.pres.values)

    df["model_temp"] = ds.thetao.values[time_idx, depth_idx, lat_idx, lon_idx]
    df["model_salt"] = ds.so.values[time_idx, depth_idx, lat_idx, lon_idx]
    return df


if __name__ == "__main__":
    df = match_argo_to_model()
    print(df[["time", "latitude", "longitude", "pres", "temp", "model_temp", "psal", "model_salt"]].head())
