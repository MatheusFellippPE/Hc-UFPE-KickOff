from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from demands.views import list_create_demands, hub_forum, react_post, comment_post  # import da view dinâmica
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", TemplateView.as_view(template_name="landing.html"), name="landing"),
    path("home/", list_create_demands, name="home"),  # agora aceita POST
    path("demandas/", include("demands.urls")),
    path("sobre-nos/", TemplateView.as_view(template_name="sobre-nos.html"), name="sobre_nos"),
    # Novas páginas estáticas
    path("servicos/", TemplateView.as_view(template_name="servicos.html"), name="servicos"),
    path("artigos/", TemplateView.as_view(template_name="artigos.html"), name="artigos"),
    path("hub/", hub_forum, name="hub"),
    path("hub/react/<int:post_id>/", react_post, name="react_post"),  # novo endpoint
    path("hub/comment/<int:post_id>/", comment_post, name="comment_post"),  # novo endpoint para comentários
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
