import dataspace

from trades.models import Trade


def activity_chart(export_path: str):
    # load all
    qs = Trade.objects.all()  # type: ignore
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
    sell_chart = sell.area_().color("indianred").opacity(0.5)  # type: ignore
    # export
    endchart = sell_chart + buy_chart  # type: ignore
    endchart.save(export_path + "/activity_chart.png")


def markets_charts(export_path: str):
    # load data
    qs = Trade.objects.all()[:1000]  # type: ignore
    ds = dataspace.from_django(qs)
    # transform
    ds.sort("date")
    ds.to_str("date")
    # chart
    ds.axis("date:T", "price:Q")
    c = ds.point_(
        encode={
            "shape": "market:N",
            "color": "side:N",
            "tooltip": ["side:N", "price:Q", "market:N"],
        }
    )
    c2 = (
        ds.square_(
            encode={"color": "side:N", "tooltip": ["side:N", "price:Q", "market:N"]}
        )
        .wh(350, 100)  # type: ignore
        .facet(facet="market:N", columns=3)
    )
    # export
    c.save(export_path + "/all_markets.png")  # type: ignore
    c2.save(export_path + "/faceted_markets.png")
