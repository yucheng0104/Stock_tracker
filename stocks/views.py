from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Stock
# Create your views here.

@login_required
def stock_list(request):
    stocks = Stock.objects.filter(user=request.user)
    return render(request, 'stocks/stock_list.html', {'stocks': stocks})