from django.contrib import admin
from .models import (Service,
                     CarModel,
                     Car,
                     Order,
                     OrderLine)

class CarAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'license_plate', 'vin_code', 'client_name']

class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'status']
    inlines = [OrderLineInLine]

# Register your models here.
admin.site.register(Service)
admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
