from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_user, user_registration, logout_user


urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', user_registration, name='register'),
    path('logout/', logout_user, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'user/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html',success_url='/user/password-reset/complete/'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'user/password_reset_complete.html'), name='password_reset_complete'),
]