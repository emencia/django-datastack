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
# # Create basic charts
#
# This notebook describes how to make basic charts. In this example we will visualize the number of buy orders on the Binance market by minutes

# %%
# %run __init__
import dataspace
from trades.models import Trade

# define the django query and load it
qs = Trade.objects.filter(market="Binance", side="buy").order_by("date")[:50000]
ds = dataspace.from_django(qs)  
ds.sort("date")
ds.show()

# %%
# we resample the data by periods of one minute for convenience
ds.rsum("date", "1m", "quantity")
ds.rename("count", "num_ops")
ds.show()

# %% [markdown]
# ## Bokeh charts
#
# Let's create a simple line with the Bokeh chart rendering engine. First we need to define the columns to use for the x and y chart's axis

# %%
ds.bokeh()
ds.axis("date", "num_ops")
ds.line_()

# %% [markdown]
# We can use different types of charts to visualize the data

# %%
ds.area_()

# %%
ds.point_()

# %%
ds.bar_(xrotation=45)

# %% [markdown]
# ### Histogram and mean line
#
# Add an histogram and mean line to a basic chart

# %%
hline = ds.hline_()
ds.point_().hist() * hline

# %% [markdown]
# ## Altair charts
#
# Use the Altair rendering engine to make the charts

# %%
# convert the datetime column to string for Altair to chart it
ds.to_str("date")
# switch to Altair rendering engine
ds.altair()
# the axis definition must include the type of the axis: here x is T for temporal
# and y is Q for quantitative
# reference: https://altair-viz.github.io/user_guide/encoding.html#encoding-data-types
ds.axis("date:T", "num_ops:Q")

# %%
ds.line_()

# %%
ds.area_()

# %%
ds.point_()

# %%
ds.bar_()

# %% [markdown]
# ### More charts
#
# Add numbers values to the chart

# %%
c = ds.line_num_()
c

# %% [markdown]
# Compose a chart with quantity bars

# %%
c2 = ds.bar_("date:T", "quantity:Q").color("red")
c + c2

# %%
