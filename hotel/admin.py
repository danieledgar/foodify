from django.contrib import admin
from .models import Hotel,Menu,Cart, CartItem, Order, OrderItem

# Register your models here.
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name','location','phone']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title','price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','created_at','updated_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','menu_item','quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','status','created_at','updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['menu_item','quantity','price']
