from django.urls import path
from .views import add_hotel, hotel_home, add_menu, MenuListView, MenuUpdateView, MenuDeleteView,hotel_orders, hotel_not_found

urlpatterns = [
    path('add_hotel', add_hotel ,name='add-hotel'),
    path('menu_list', MenuListView.as_view() ,name='menu-list'),
    path('menu_update/<pk>', MenuUpdateView.as_view() ,name='menu-update'),
    path('menu_delete/<pk>', MenuDeleteView.as_view() ,name='menu-delete'),
    path('add_menu', add_menu ,name='add-menu'),
    path('hotel_orders', hotel_orders ,name='orders'),
    path('hotel_not_found', hotel_not_found ,name='hotel_not_found'),
    path('', hotel_home ,name='hotel-home'),
]
