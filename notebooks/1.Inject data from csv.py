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
# # Inject data into the database from csv
#
# This notebook shows how to use the Django orm to inject data coming from a csv file

# %%
# %run __init__
import dataspace
from trades.models import Trade

ds = dataspace.from_csv("data/BTC-USDT-1min.csv")
ds.show()

# %% [markdown]
# Now we iterate over the data and hit a save query for each datapoint

# %%
for row in ds.df.rows(named=True):
    Trade.objects.create(date=row["mktTS"],price=row["px"],quantity=row["qty"],side=row["side"].lower(),market=row["Source"])
print("ok")

# %%
qs = Trade.objects.all()
ds = dataspace.from_django(qs)
ds.show()

# %%
Trade.objects.all().delete()

# %%
