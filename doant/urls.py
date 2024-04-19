from django.contrib.auth import views as auth_views
from django.urls import path  # Make sure to import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user_details/', views.user_details, name='user_details'),
    path('donate/', views.donate, name='donate'),
    path('donation_statistics/', views.donation_statistics, name='donation_statistics'),
    path('donate/success/', views.donate_success, name='donate_success'),   
]
