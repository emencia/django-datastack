# Django data analytics stack

This repository shows a Django data analytics stack

## Available notebooks

- **Inject data from csv**: see how to inject some data into the database from csv files
- **Batch insert data from csv**: see how to inject large amounts of data into the database
from csv files with a progress bar
- **Query data**: see how to query the database and get a dataframe
- **Compose charts**: see how to prototype charts in notebooks from dataframes
- **Export and serve charts**: see how to create a charts generation pipeline and serve the charts

## Install

Clone the repository and install:

```
make install
```

This will create a virtualenv locally, create an Sqlite db and run the migrations

## Notebooks

Open the notebooks app in a django env:

```
make notebooks
```

All the notebooks are located in the `notebooks` directory. Note for version control: the
notebooks are paired to .py files that are used for version control. The .ipynb files will
not be pushed to the git repository. See the git workflow section below

To open a notebook from a Python file right click on it and select "Open as a notebook"

### Git workflow

Create notebooks and pair them to .py files when you want to share it
with git. To pair a notebook see [the doc](https://github.com/mwouts/jupytext/blob/master/docs/paired-notebooks.md#paired-notebooks)
and use the *Pair Notebook with percent script* command. Once paired a notebook can be commited.

To open the command panel on Jupyterlab use the Ctrl-Shift-C command and type *jup*

## Data pipeline

To run the data pipeline and generate the charts:

```
make pipeline
```

To run the Django dev server:

```
make run
```