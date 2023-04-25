# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Django Shell-Plus
#     language: python
#     name: django_extensions
# ---

# %% [markdown]
# # Batch insert a large csv
#
# This notebooks presents how to batch insert a large quantity of data into the database. A progress bar widget is provided

# %%
# %run __init__
import polars as pl
from ipywidgets import IntProgress
from IPython.display import display
import dataspace
from trades.models import Trade

ds = dataspace.from_csv("data/bitcoin1.csv")
ds2 = dataspace.from_csv("data/bitcoin2.csv")
ds.df = pl.concat([ds.df, ds2.df], rechunk=True)
ds.show()

# %%
num_objs = len(ds.df)

# progress bar
progress = IntProgress(min=0, max=num_objs)
display(progress)

batch_size = 999
objs = []
i = 0
ii = 0
# iterate on the data
for row in ds.df.rows(named=True):
    t = Trade(date=row["mktTS"],price=row["px"],quantity=row["qty"],side=row["side"].lower(),market=row["Source"])
    objs.append(t)
    i+=1
    if (i==batch_size):
        # print(ii+1, "saving batch")
        Trade.objects.bulk_create(objs)
        objs = []
        i = 0
        progress.value = ii
    ii+=1
# save the remaining objects
if (len(objs)>0):
    Trade.objects.bulk_create(objs)
    
progress.close()

print("Ok, inserted", Trade.objects.all().count(), "objects")

# %%
#Trade.objects.all().delete()

# %%
