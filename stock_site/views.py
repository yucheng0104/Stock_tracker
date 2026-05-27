from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 儲存新使用者並直接登入，不需要再跳去登入頁
            user = form.save()
            login(request, user)
            return redirect('stock_list')
    else:
        # 第一次進頁面，顯示空白註冊表單
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})