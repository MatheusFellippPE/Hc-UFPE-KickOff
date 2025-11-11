from django.urls import path
from .views import list_create_demands

urlpatterns = [
    path("", list_create_demands, name="demandas"),
]
