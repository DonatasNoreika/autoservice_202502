from django.contrib import admin
from .models import (Service,
                     CarModel,
                     Car,
                     Order,
                     OrderLine,
                     OrderComment,
                     Profile)

class CarAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'license_plate', 'vin_code', 'client_name']
    list_filter = ['car_model', 'client_name']
    search_fields = ['license_plate', 'vin_code']

class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ['service', 'quantity', 'line_sum']
    readonly_fields = ['line_sum']

class OrderCommentInLine(admin.TabularInline):
    model = OrderComment
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'car', 'date', 'deadline', 'status', 'total_sum', 'is_overdue']
    inlines = [OrderLineInLine, OrderCommentInLine]

    fieldsets = (
        ('General', {'fields': ('client', 'date', 'deadline', 'car', 'status', 'total_sum')}),
    )

    readonly_fields = ['date', 'total_sum']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'service__price', 'quantity', 'line_sum']

# Register your models here.
admin.site.register(Service, ServiceAdmin)
admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Profile)