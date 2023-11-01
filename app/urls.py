from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import UserProfileCreateView


urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('signin/', views.signin, name="signin"),
    path('logout/',auth_views.LogoutView.as_view(),name="logout"),
    path('about/', views.about, name="about"),
    path('userhome/', views.userhome, name="userhome"),

    path('adminpanel/', views.admin_dashboard, name='admin_dashboard'),
    path('userhome/goalsetting/', views.user_goal_setting_view, name='user_goal_setting'),
    path('userprofile/', UserProfileCreateView.as_view(), name='userprofile'),

    path('trainerdetails/', views.trainerdetails, name='trainerdetails'),
    path('nutritiondetails/', views.nutritiondetails, name='nutritiondetails'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('goalsetting/', views.display_goals, name='goalsetting'),  # Display the goal-setting page
    path('save_fitness_goal/', views.save_fitness_goal, name='save_fitness_goal'),  # Save fitness goals
    path('trainerreg/', views.trainerreg, name='trainerreg'),

    


    path('dashboardbase/', views.dashboardbase, name="dashboardbase"),
    path('userdetails/', views.userdetails, name="userdetails"),
    path('userhome/usertrainer/', views.usertrainer, name='usertrainer'),
    path('userhome/usernutrition/', views.usernutrition, name='usernutrition'),
    path('classess/', views.classess, name="classess"),
    path('content/', views.content, name="content"),
   
    path('nutritionreg/', views.nutritionreg, name="nutritionreg"),


    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

 
] 
