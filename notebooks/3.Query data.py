# -*- coding: utf-8 -*-
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
# # Query data with django
#
# This notebook describes how to query the database and get a dataframe

# %%
# %run __init__
import dataspace
from trades.models import Trade

qs = Trade.objects.all()[:5000]
ds = dataspace.from_django(qs)    
ds.show()

# %% [markdown]
# Let's get just the sells:

# %%
qs = Trade.objects.filter(side="sell")[:5000]
ds = dataspace.from_django(qs)
ds.to_str("date")
ds.show()

# %% [markdown]
# ## Visualization
#
# Chart it and get a quick visual representation:

# %%
ds.axis("date:T", "price:Q")
ds.line_()

# %% [markdown]
# Let's say we want to see only the 50% highest offers on the sell side. Let's get the mean and filter the data

# %%
ds.df["price"].mean()

# %%
qs = Trade.objects.filter(side="sell", price__gte=ds.df["price"].mean())[:5000]
ds = dataspace.from_django(qs)    
ds.show()

# %%
ds.axis("date:T", "price:Q")
ds.to_str("date")
ds.line_()

# %%
