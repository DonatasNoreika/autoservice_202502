from django.contrib import admin
from .models import (Service,
                     CarModel,
                     Car,
                     Order,
                     OrderLine)

# Register your models here.
admin.site.register(Service)
admin.site.register(CarModel)
admin.site.register(Car)
admin.site.register(Order)
admin.site.register(OrderLine)
