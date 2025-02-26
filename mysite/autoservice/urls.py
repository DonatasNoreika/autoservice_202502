from django.urls import path
from .views import (index,
                    cars,
                    car,
                    search,
                    register,
                    profile,
                    OrderListView,
                    OrderDetailView,
                    UserOrderListView,
                    OrderCreateView)

urlpatterns = [
    path("", index, name="index"),
    path("cars/", cars, name="cars"),
    path("cars/<int:car_id>", car, name="car"),
    path("search/", search, name="search"),
    path("user_orders/", UserOrderListView.as_view(), name="user_orders"),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order"),
    path("orders/new", OrderCreateView.as_view(), name="orders_new"),
]
