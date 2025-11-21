from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .forms import RegistrationForm, EmailLoginForm
from .models import Profile
import jwt, datetime
from django.conf import settings

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"].lower()
            user_type = form.cleaned_data["user_type"]
            password = form.cleaned_data["password"]

            if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
                form.add_error("email", "Email já cadastrado.")
            else:
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=name,
                    )
                    Profile.objects.create(user=user, user_type=user_type)
                messages.success(request, "Registro realizado com sucesso. Você já pode fazer login.")
                next_url = request.POST.get("next") or request.GET.get("next") or "accounts:login"
                return redirect(next_url)
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    # determina para onde redirecionar após login
    next_url = request.GET.get("next") or request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # gera JWT simples para identificação adicional (opcional)
                payload = {
                    "uid": user.id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
                    "iat": datetime.datetime.utcnow(),
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
                response = redirect(next_url)
                response.set_cookie(
                    "auth_token",
                    token,
                    httponly=True,
                    samesite="Lax",
                    secure=not settings.DEBUG,
                )
                return response
            form.add_error(None, "Email ou senha inválidos.")
    else:
        form = EmailLoginForm()
    return render(request, "login.html", {"form": form, "next": next_url})


@require_http_methods(["POST", "GET"])
def logout_view(request):
    """
    Encerra a sessão do usuário e redireciona para 'next' (ou landing '/'). Remove JWT.
    """
    logout(request)
    next_url = request.POST.get("next") or request.GET.get("next") or "/"
    response = redirect(next_url)
    response.delete_cookie("auth_token")
    return response
