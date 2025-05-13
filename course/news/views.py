from django.shortcuts import render, redirect
from .models import Funcs,  Features
from .forms import FuncsForm, FeaturesForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
def news_home(request):
    features = Features.objects.all()
    return render(request, 'news/features.html', {'features': features})
def create(request):
    if request.method == "POST":
        form = FuncsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'news/create.html', {'form': form, 'error': 'Неверное заполнение формы'})

    form = FuncsForm()


    return render(request, 'news/create.html', {'form': form})


def features_list(request):
    features = Features.objects.all()
    return render(request, 'news/features.html', {'features': features})

def create_feature(request):
    if request.method == "POST":
        form = FeaturesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('features_list')

    form = FeaturesForm()
    return render(request, 'news/create_feature.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправление на главную страницу после входа
    else:
        form = AuthenticationForm()
    return render(request, 'news/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = UserCreationForm()
    return render(request, 'news/register.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'main/home.html')

