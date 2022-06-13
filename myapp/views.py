from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import SampleUser

def login_func(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        
        else:
            return render(request, 'login.html', {})

    return render(request, 'login.html',{})

@login_required
def index_func(request):
    return render(request, 'index.html', {})

@login_required
def app1_func(request, pk):
    user = SampleUser.objects.get(pk=pk)
    if user.role == 'leader':
        return render(request, 'index.html', {})
    
    return render(request, 'index.html', {})

@login_required
def app2_func(request, pk):
    user = SampleUser.objects.get(pk=pk)
    if not user.role == 'normal':
        return render(request, 'app2.html', {})
    
    return render(request, 'index.html', {})

@login_required()
def app3_func(request, pk):
    user = SampleUser.objects.get(pk=pk)
    if not user.role == 'normal':
        return render(request, 'app3.html', {})

    return render(request, 'index.html', {})