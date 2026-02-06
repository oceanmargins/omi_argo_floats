
# Python scripts to process and analyze Argo floats


## Opening GitHub notebooks in Colab
It is possible to open the .ipynb files directly from GitHub in Colab:

[https://colab.research.google.com/github/oceanmargins/omi_argo_floats/blob/main/argo_pandas.ipynb]

Replace github.com with colab.research.google.com/github in your notebook URL
Example: github.com/username/repo/blob/main/notebook.ipynb becomes colab.research.google.com/github/username/repo/blob/main/notebook.ipynb
Or use Colab's UI: File → Open notebook → GitHub tab, then paste your repo URL
Students can click a link and start coding immediately without cloning anything

## Saving changes back to GitHub
You can push changes back, but it requires a few steps:

Use !git commands in Colab cells to commit and push (requires authentication)
Or manually download the notebook and push it yourself
Or use Colab's "Save a copy to GitHub" feature (File menu)

## Better workflow for education
Most educators use a hybrid approach:

Keep notebooks in GitHub (version control, easy sharing)
Have students open them in Colab (no setup friction)
Students save their work to their own Google Drive or fork the repo

## Considerations

Colab-to-GitHub is slightly clunky for frequent saves—GitHub isn't the primary storage
If you want tight version control, students might fork the repo and push changes back themselves
For a one-way "read-only" setup (you maintain notebooks, students use them), it's seamless

For most classes, you'd just host notebooks on GitHub and share Colab links. The integration is smooth enough that students never need to touch GitHub directly if you don't want them to.


GitHub as primary - Store notebooks in your repo with proper version control and branches
Open notebooks in Colab - Same easy URL trick, but now you're working from controlled versions
Save work back systematically - This becomes more important:

Use Colab's "Save a copy to GitHub" feature and commit properly
Or use !git commands in cells to push directly from Colab
Or develop locally and push to GitHub, using Colab only for exploration/computation



## Key considerations for research teams
Data management - This is critical and often overlooked:

Don't store data in GitHub (too large, inefficient)
Use separate storage: cloud storage (Google Drive, S3), databases, or a shared data folder
Document data locations and access in your README
Use environment variables or config files to reference data paths

## Environment reproducibility - More important for research:

Create requirements.txt or environment.yml in your repo
Pin dependency versions
In Colab, add a setup cell: !pip install -r requirements.txt
This ensures everyone runs the same code

## Collaboration patterns:

Use branches for individual work, PRs for review before merging
Colab's real-time collaboration (File → Share) works but isn't ideal for version control—better to use GitHub
Document your methodology in notebooks clearly

## Beyond Colab - when to consider alternatives:

If you need reproducible environments with specific OS/system dependencies → Docker
If you're training large models repeatedly → experiment tracking tools (MLflow, Weights & Biases)
If notebooks become too large/complex → move to Python scripts + Jupyter for exploration
If you need persistent servers → JupyterHub or cloud instances

Practical research setup
your-repo/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_model_training.ipynb
├── src/
│   └── helper_functions.py
├── data/
│   └── README.md (explains where data lives)
├── requirements.txt
└── README.md (methodology, results, how to run)
Students open notebooks from GitHub links in Colab, but you manage versions and data separately. For actual development work, your team likely commits refined code back to GitHub.
One more thing: For research, you might eventually want to track experiments (hyperparameters, results, computational cost). Tools like Weights & Biases integrate nicely with Colab and pair well with GitHub-based notebooks.
Is your team doing exploratory work mainly (notebooks as primary), or moving toward more structured ML/research code?
