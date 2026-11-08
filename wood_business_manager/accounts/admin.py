from django.contrib import admin
from .models import Customer, WoodType, Sale, Payment

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at")
    search_fields = ("name", "phone")

@admin.register(WoodType)
class WoodTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "quantity", "purchase_rate")

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("date", "customer", "wood_type", "quantity", "total_amount")
    list_filter = ("date", "wood_type")
    search_fields = ("customer__name",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("date", "customer", "amount", "method")
    list_filter = ("date", "method")
    search_fields = ("customer__name",)
