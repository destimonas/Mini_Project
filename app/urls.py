from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('signin/', views.signin, name="signin"),
    path('signout/',views.signout,name="signout"),
    path('about/', views.about, name="about"),

    path('userhome/', views.userhome, name="userhome"),



    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

 
] 
