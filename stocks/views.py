from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Stock
# Create your views here.

@login_required
def stock_list(request):
    stocks = Stock.objects.filter(user=request.user)
    return render(request, 'stocks/stock_list.html', {'stocks': stocks})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('stock_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})