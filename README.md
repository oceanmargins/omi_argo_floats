
# Python scripts to process and analyze Argo floats


## Opening GitHub notebooks in Colab

You can open the notebook directly from GitHub in Google Colab without any local setup:

[https://colab.research.google.com/github/oceanmargins/omi_argo_floats/blob/main/argo_pandas.ipynb]

You need a GitHub account and a Google account.


## Local setup with pixi

[pixi](https://pixi.sh) is a fast, cross-platform package manager. It handles Python and conda dependencies in one step.

### 1. Install pixi

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

Restart your terminal after installation, or source your shell profile to make the `pixi` command available.

### 2. Clone this repository

```bash
git clone https://github.com/oceanmargins/omi_argo_floats.git
cd omi_argo_floats
```

### 3. Install the project environment

```bash
pixi install
```

This reads `pyproject.toml` and installs all dependencies (NumPy, pandas, xarray, matplotlib, argopy, JupyterLab, etc.) into an isolated environment — no `conda activate` or `pip install` needed.

### 4. Start JupyterLab

```bash
pixi run jupyter lab
```

JupyterLab will open in your browser. Open `argo_pandas.ipynb` from the file browser on the left.


## Using the notebook

The notebook `argo_pandas.ipynb` fetches Argo float data from the [IFREMER ERDDAP server](https://erddap.ifremer.fr/erddap/tabledap/ArgoFloats.html) and loads it into a pandas DataFrame for analysis.

**Workflow:**

1. **Configure the query** — The notebook builds an ERDDAP URL to select a specific float (`fileNumber`) and a geographic bounding box (latitude/longitude range). Edit these values in the second cell to target a different float or region.

2. **Fetch data** — `pd.read_csv(url, skiprows=[1])` downloads the data directly from ERDDAP into a DataFrame. Columns include `time`, `latitude`, `longitude`, `pres` (pressure/depth), `temp`, `psal` (salinity), `doxy`, `turbidity`, `chla`, and `nitrate`.

3. **Explore and plot** — The notebook demonstrates a temperature–salinity scatter plot and a map of the float track. Adapt these cells for your own analysis.

**To query a different float:**

Go to [https://erddap.ifremer.fr/erddap/tabledap/ArgoFloats.html] to browse available floats and build a custom ERDDAP URL, then paste it into the notebook.


## Downloading model and wind data

Several scripts in this repo download external reanalysis/forecast data used to compare against Argo observations. They all save into a local `data/` directory (created automatically, and git-ignored).

### `myocean.py`

Downloads salinity and temperature fields from the [Copernicus Marine Service](https://marine.copernicus.eu/) (CMEMS) global ocean physics analysis/forecast product (`cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m` / `...-thetao_...`).

- `login(username, password)` — authenticates with Copernicus Marine using `copernicusmarine.login`. Requires a free Copernicus Marine account.
- `retrieve(data_var="salt")` — subsets and downloads one variable (`"salt"` or `"temp"`) as NetCDF into `data/`. The bounding box, date range, and depth range are currently hardcoded in the function.

Running the module directly (`pixi run python myocean.py`) downloads both salinity and temperature.

### `copernicus.ipynb`

A scratch notebook covering the same Copernicus Marine workflow interactively: logging in, subsetting a small region (currents, salinity, temperature) as Zarr, loading it with `xarray`, and plotting it with `matplotlib`/`cartopy` (salinity color maps, current streamplots, coastlines). Useful as a starting point for exploring a new CMEMS subset before scripting it.

Note: `cartopy` is used for the map plots in this notebook but is not yet listed in `pyproject.toml`; install it into the pixi environment if you want to run those cells.

### `winds.py`

Downloads ERA5 wind data and reads met-tower data used alongside the Argo/CMEMS comparisons.

- `download_era5(variable="10m_u_component_of_wind")` — downloads a full year (`YEAR`) of 6-hourly ERA5 reanalysis data over a fixed bounding box (`AREA`) via the [CDS API](https://cds.climate.copernicus.eu/), saving a `.grib` file into `data/`. Requires a CDS API key configured (typically in `~/.cdsapirc`).
- `read_mettower()` — fetches the OMI Ghana meteorological tower JSON feed and returns it as a DataFrame with a parsed `time` column.
- `retrieve()` — downloads both u/v wind components and the met-tower data, saving the latter to `data/met_tower_data.h5`.

### `match_argo_model.py`

Matches each Argo profile observation to the nearest CMEMS model grid cell, for direct comparison of observed vs. modeled temperature and salinity.

- Reads Argo data from `data/argo_data.h5` and the most recent `*phy-thetao_*.nc` / `*phy-so_*.nc` files in `data/` (as produced by `myocean.py`).
- `match_argo_to_model(argo_file=ARGO_FILE, temp_file=None, salt_file=None)` — for each Argo row, finds the nearest model grid point in latitude/longitude (via a `scipy.spatial.cKDTree`), and the nearest model time step and depth level (via a sorted nearest-value search), then adds `model_temp` and `model_salt` columns to the returned DataFrame.
- Running the module directly (`pixi run python match_argo_model.py`) prints a preview comparing Argo `temp`/`psal` to the matched `model_temp`/`model_salt`.

### `data/argo_data_with_model.csv`

The CSV export of `match_argo_to_model()`'s output — one row per Argo profile observation, with columns `fileNumber`, `time`, `latitude`, `longitude`, `pres`, `temp`, `psal`, `doxy`, `turbidity`, `chla`, `nitrate` (from Argo) plus `model_temp` and `model_salt` (the matched CMEMS values) for direct comparison.
