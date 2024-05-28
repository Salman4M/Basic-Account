from django.urls import path
from account import views


app_name='account'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('home/',views.home_view,name='home'),
    path('register/',views.register_view,name='register'),
    path('activation/<uuid>/',views.activation_view,name='activation'),
    path('reset_password/',views.reset_password_view,name='reset-password'),
    path('reset_complete/<uuid>/',views.reset_password_code_view,name='reset-code'),
    path('reset_complete_done/<uuid>/<token>/',views.reset_password_complete,name='reset-password-complete'),
    path('change_password/',views.change_password_view,name='change-password'),
    
]
