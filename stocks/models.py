from django.db import models
from django.contrib.auth.models import User
import yfinance as yf
# Create your models here.

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"
    
    # 用 yfinance 取得目前股價
    def get_current_price(self):
        try:

            symbol = f"{self.symbol}.TW" if self.symbol[0].isdigit() else self.symbol
            ticker = yf.Ticker(symbol)
            data = ticker.fast_info
            return round(data.last_price, 2)
        except Exception :
            return None