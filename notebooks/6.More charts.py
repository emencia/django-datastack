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
# ## More complex charts
#
# In this section we will improve the charts to get a better data visualization

# %%
# %run __init__
import dataspace
from trades.models import Trade

# define the django query and load it
qs = Trade.objects.all()[:1000]
ds = dataspace.from_django(qs)  
ds.sort("date")
ds.to_str("date")
ds.show()

# %% [markdown]
# ## View all markets in one chart

# %%
ds.axis("date:T", "price:Q")
c = ds.point_(encode={"shape":'market:N', "color":"side:N", 'tooltip': ['side:N','price:Q', 'market:N']})
c

# %% [markdown]
# ## Faceted view of all markets

# %%
ds.square_(encode={"color":"side:N", 'tooltip': ['side:N','price:Q', 'market:N']}).wh(350,100).facet(
    facet='market:N',
    columns=3
)
