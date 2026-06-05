from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Stock
from .forms import StockForm
import yfinance as yf
import plotly.graph_objs as go
from plotly.offline import plot

# Create your views here.


@login_required
def stock_list(request):
    # 只撈出屬於目前使用者的股票資料
    stocks = Stock.objects.filter(user=request.user)
    # 為每筆股票加上即時股價
    for stock in stocks:
        stock.current_price = stock.get_current_price()
    return render(request, "stocks/stock_list.html", {"stocks": stocks})


@login_required
def stock_create(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            # commit=False 先不存入資料庫，因為還需要補上 user 欄位
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()
            return redirect("stock_list")
    else:
        # 第一次進頁面，顯示空白表單
        form = StockForm()
    return render(request, "stocks/stock_form.html", {"form": form})


@login_required
def stock_edit(request, pk):
    # 找到指定的股票，確保只能編輯自己的股票
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == "POST":
        # 把使用者填的資料放進表單，instance 代表編輯現有資料
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect("stock_list")
    else:
        # 第一次進頁面，預先填入現有資料
        form = StockForm(instance=stock)
    return render(request, "stocks/stock_form.html", {"form": form})


@login_required
def stock_delete(request, pk):
    # 找到指定的股票，確保只能刪除自己的股票，找不到回傳 404 頁面
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == "POST":
        # 確認 POST 後才執行刪除動作，避免使用者誤觸連結就刪除資料
        stock.delete()
        return redirect("stock_list")
    return render(request, "stocks/stock_confirm_delete.html", {"stock": stock})


@login_required
def stock_detail(request, pk):
    # 找到指定的股票，確保只能查看自己的資料
    stock = get_object_or_404(Stock, pk=pk, user=request.user)

    period = request.GET.get("period", "1mo")  # 預設為最近一個月

    # 判斷台股或美股
    symbol1 = f"{stock.symbol}.TW" if stock.symbol[0].isdigit() else stock.symbol

    # 使用 yfinance 取得歷史股價資料
    ticker = yf.Ticker(symbol1)
    hist = ticker.history(period=period)

    # 繪製股價走勢圖
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=hist.index,
                open=hist["Open"],
                high=hist["High"],
                low=hist["Low"],
                close=hist["Close"],
            )
        ]
    )

    fig.update_layout(
        title=f"{stock.symbol} - ({stock.name}) 股價走勢圖",
        xaxis_title="日期",
        yaxis_title="價格",
        xaxis_rangeslider_visible=False,
    )

    chart = plot(fig, output_type="div")

    stock.current_price = stock.get_current_price()
    return render(
        request,
        "stocks/stock_detail.html",
        {
            "stock": stock,
            "chart": chart,
            "period": period,
        },
    )
