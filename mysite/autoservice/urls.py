from django.urls import path
from .views import index, cars

urlpatterns = [
    path("", index, name="index"),
    path("cars/", cars, name="cars"),
]
