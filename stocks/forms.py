from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['symbol', 'name', 'buy_price']
        labels = {
            'symbol': '股票代碼',
            'name': '股票名稱',
            'buy_price': '購買價格',
        }