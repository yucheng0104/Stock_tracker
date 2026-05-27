from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Stock
from .forms import StockForm
# Create your views here.

@login_required
def stock_list(request):
    # 只撈出屬於目前使用者的股票資料
    stocks = Stock.objects.filter(user=request.user)
    return render(request, 'stocks/stock_list.html', {'stocks': stocks})



@login_required
def stock_create(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            # commit=False 先不存入資料庫，因為還需要補上 user 欄位
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()
            return redirect('stock_list')
    else:
        # 第一次進頁面，顯示空白表單
        form = StockForm()
    return render(request, 'stocks/stock_form.html', {'form': form})    

@login_required
def stock_edit(request, pk):
    # 找到指定的股票，確保只能編輯自己的股票
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == 'POST':
        # 把使用者填的資料放進表單，instance 代表編輯現有資料
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        # 第一次進頁面，預先填入現有資料
        form = StockForm(instance=stock)
    return render(request, 'stocks/stock_form.html', {'form': form})