from django.core.management.base import BaseCommand
from trades.pipeline import run as run_pipeline


class Command(BaseCommand):
    help = "Run the data pipeline ang generate the charts"

    def handle(self, *args, **options):
        verbose = options["verbosity"] == 1
        if verbose:
            print("Running data pipeline")
        run_pipeline(verbose=verbose)
        if verbose:
            print("Finished running data pipeline")
