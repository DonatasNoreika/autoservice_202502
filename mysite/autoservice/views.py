from django.shortcuts import render
from .models import Service, Order, Car


# Create your views here.
def index(request):
    num_services = Service.objects.all().count()
    num_orders_done = Order.objects.filter(status="i").count()
    num_cars = Car.objects.all().count()
    context = {
        'num_services': num_services,
        'num_orders_done': num_orders_done,
        'num_cars': num_cars,
    }
    return render(request, template_name="index.html", context=context)


def cars(request):
    context = {"cars": Car.objects.all()}
    return render(request, template_name="cars.html", context=context)