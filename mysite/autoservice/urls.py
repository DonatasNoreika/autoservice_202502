from django.urls import path
from .views import index, cars, car, OrderListView

urlpatterns = [
    path("", index, name="index"),
    path("cars/", cars, name="cars"),
    path("cars/<int:car_id>", car, name="car"),
    path("orders/", OrderListView.as_view(), name="orders"),
]
