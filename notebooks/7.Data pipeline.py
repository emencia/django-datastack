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
# # Create a data pipeline
#
# We will now create some functions to assemble a data pipeline that can run as a management command. 
#
# It will use some of the previously prototyped charts and export them to png images, so that we can integrate them in the frontend

# %%
# %run __init__
import dataspace
from trades.models import Trade

def activity_chart(export_path: str):
    # load all
    qs = Trade.objects.all()
    ds = dataspace.from_django(qs)
    # split
    dss = ds.split_("side")
    sell = dss["sell"]
    buy = dss["buy"]
    # resample
    buy.sort("date")
    buy.rsum("date", "1m")
    buy.rename("count", "num_ops")
    buy.show()
    sell.sort("date")
    sell.rsum("date", "1m")
    sell.rename("count", "num_ops")
    # chart
    buy.to_str("date")
    sell.to_str("date")
    buy.axis("date:T", "num_ops:Q")
    sell.axis("date:T", "num_ops:Q")
    buy_chart = buy.line_().color("green")
    sell_chart = sell.area_().color("indianred").opacity(0.5)
    # export
    endchart = sell_chart + buy_chart
    endchart.save(export_path+"activity_chart.png")
    
activity_chart("./")


# %%
def markets_charts(export_path: str):
    # load data
    qs = Trade.objects.all()[:1000]
    ds = dataspace.from_django(qs)  
    # transform
    ds.sort("date")
    ds.to_str("date")
    # chart
    ds.axis("date:T", "price:Q")
    c = ds.point_(encode={
        "shape":'market:N', "color":"side:N", 'tooltip': ['side:N','price:Q', 'market:N']
    })
    c2 = ds.square_(encode={
        "color":"side:N", 'tooltip': ['side:N','price:Q', 'market:N']
    }).wh(350,100).facet(
        facet='market:N',
        columns=3
    )
    # export
    c.save(export_path + "all_markets.png")
    c2.save(export_path + "faceted_markets.png")
    
markets_charts("./")

# %% [markdown]
# ## Management command
#
# Now we will copy these functions to a data pipeline that will run using a management command to generate the chart images. We will integrate the images in templates
#
# Check the `datastack/trades/pipeline/charts.py` file
