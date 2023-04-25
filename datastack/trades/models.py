from django.db import models

SIDE = [("buy", "buy"), ("sell", "sell")]


class Trade(models.Model):
    date = models.DateTimeField()
    price = models.FloatField()
    quantity = models.FloatField()
    market = models.CharField(max_length=255)
    side = models.CharField(max_length=4, choices=SIDE)

    def __str__(self) -> str:
        return f"${self.market} ${self.date}"
