from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.utils import delete_sale_with_no_items


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(
                request,
                'Erro ao acessar. Verifique seu usuário e/ou senha.',
                extra_tags='danger'
                )
            return redirect('login')
    return render(request, 'login.html')


def logout_view(request):

    delete_sale_with_no_items(request=request)

    if 'sale_id' in request.session:
        messages.error(
            request,
            '''Erro ao fazer logout:
            você possui uma venda em aberto,
            finalize-a para sair do sistema''',
            extra_tags='danger'
        )
        return redirect('start_sale')

    logout(request)
    return redirect('login')
