
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
