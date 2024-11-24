from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import translation

from .forms import CustomLoginForm, CustomRegisterForm
from .models import UserProfile


@login_required
def index_view(request):
    translation.activate(request.session["language"])
    return render(request, "index.html")


def login_view(request):
    form = CustomLoginForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)

        user_profile = UserProfile.objects.get(user=user)
        language_code = user_profile.language

        request.session["language"] = language_code
        translation.activate(language_code)
        return redirect("index")
    return render(request, "pages-login.html", {"form": form})


def register_view(request):
    form = CustomRegisterForm(data=request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)  # Đăng nhập sau khi đăng ký thành công
        user_profile = UserProfile.objects.get(user=user)
        language_code = user_profile.language
        request.session["language"] = language_code
        translation.activate(language_code)
        return redirect("index")
    return render(request, "pages-register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def change_language(request):
    language_code = request.POST.get("language", "en")
    translation.activate(language_code)
    request.session["language"] = language_code
    return redirect("index")
