from django.urls import path
from .views import callback, waiting_page, check_status, payment_failed, payment_cancelled

urlpatterns = [
     path('callback/', callback, name = 'awaiting-callback'),
     path('waiting/<str:transaction_id>/', waiting_page, name='waiting-page'),
     path('check_status/<str:transaction_id>/', check_status, name='check_status'),
     path('payment-failed/', payment_failed, name='payment_failed'),
     path('payment-cancelled/', payment_cancelled, name='payment_cancelled'),
]
