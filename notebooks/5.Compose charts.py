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
# # Charts composition
#
# It is possible to combine severall charts and merge them. Let's load all the data

# %%
# %run __init__
import dataspace
from trades.models import Trade

# define the django query and load it
qs = Trade.objects.all()
ds = dataspace.from_django(qs)
ds.show()

# %% [markdown]
# ## Split data by side
#
# We split the data by side in order to compose lines for each side

# %%
dss = ds.split_("side")
sell = dss["sell"]
buy = dss["buy"]
sell.show()

# %% [markdown]
# ## Resample the data
#
# We now resample the data to group it by periods of one minute, more than 400 000 rows is too much for a chart

# %%
# we resample and sum the data by periods of one minute for convenience
buy.sort("date")
buy.rsum("date", "1m")
buy.rename("count", "num_ops")
buy.show()

sell.sort("date")
sell.rsum("date", "1m")
sell.rename("count", "num_ops")
buy.show()

# %%
sell.show()

# %% [markdown]
# ## Combined charts
#
# Let's combine the by and sell lines in one chart

# %%
# convert the datetime column to string for Altair to chart it
buy.to_str("date")
sell.to_str("date")
# build charts
buy.axis("date:T", "num_ops:Q")
buy_chart = buy.line_().color("forestgreen")
sell.axis("date:T", "num_ops:Q")
sell_chart = sell.line_().color("crimson")
sell_chart + buy_chart

# %% [markdown]
# #### Example of rendering options
#
# Let's give more relief to the sell side

# %%
buy_chart = buy.line_().color("greenyellow")
sell_chart = sell.area_().color("indianred").opacity(0.5)
buy_chart + sell_chart

# %% [markdown]
# Let's give more relief to the buy side

# %%
buy_chart = buy.area_().color("greenyellow").opacity(0.5)
sell_chart = sell.line_().color("indianred")
sell_chart + buy_chart

# %% [markdown]
# ### Export chart data

# %%
endchart = sell_chart + buy_chart
endchart.save('chart.png')

# %%
