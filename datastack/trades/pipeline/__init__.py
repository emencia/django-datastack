from .charts import markets_charts, activity_chart
from django.conf import settings


def run(verbose: bool = False):
    path = str(settings.BASE_DIR.absolute()) + "/static/charts"
    if verbose is True:
        print("Creating markets charts")
    markets_charts(path)
    if verbose is True:
        print("Creating activity chart")
    activity_chart(path)
