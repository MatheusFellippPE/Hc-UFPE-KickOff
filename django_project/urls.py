from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from demands.views import list_create_demands  # import da view dinâmica

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", TemplateView.as_view(template_name="landing.html"), name="landing"),
    path("home/", list_create_demands, name="home"),  # agora aceita POST
    path("demandas/", include("demands.urls")),
    path("sobre-nos/", TemplateView.as_view(template_name="sobre-nos.html"), name="sobre_nos"),
    path("hub/", TemplateView.as_view(template_name="hub.html"), name="hub"),
]
