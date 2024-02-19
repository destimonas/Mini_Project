from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import UserProfileCreateView,TrainerProfileView
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('signin/', views.signin, name="signin"),
    path('logout/',views.logout_user,name="logout"),
    path('about/', views.about, name="about"),
    path('service/', views.service, name="service"),
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
    path('trainerhome/', views.trainerhome, name='trainerhome'),

    path('nutritionist/', views.nutritionist, name='nutritionist'),

    # path('specialization/', views.specialization, name='specialization'),
    path('specialization/', views.specialization_list, name='specialization_list'),
    path('specialization/create/', views.create_specialization, name='create_specialization'),

    path('specialization/delete/<int:pk>/', views.delete_specialization, name='delete_specialization'),
    path('change_password/', views.change_password, name='change_password'),
    


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


        
    path('approve_trainer/<int:trainer_id>/', views.approve_trainer, name='approve_trainer'),
    path('reject_trainer/<int:trainer_id>/', views.reject_trainer, name='reject_trainer'),

   
    path('approve_nutritionist/<int:nutritionist_id>/', views.approve_nutritionist, name='approve_nutritionist'),

    path('reject_nutritionist/<int:nutritionist_id>/', views.reject_nutritionist, name='reject_nutritionist'),

    path('specialization/update/<int:pk>/', views.update_specialization, name='update_specialization'),

    path('consult_trainer/', views.consult_trainer, name='consult_trainer'),
    
    path('trainerhome/trainerprofile/',TrainerProfileView.as_view(), name='trainerprofile'),
    
    path('trainerhome/schedule/', views.weekly_class_schedule, name='weekly_class_schedule'),

    path('save_user_profile/', views.save_user_profile, name='save_user_profile'),

    path('nutritionist/nutritionprofile/', views.nutritionprofile, name='nutritionprofile'),

    path('rate_trainer/<int:trainer_id>/', views.rate_trainer, name='rate_trainer'),

    path('addslot/', views.add_slot, name='add_slot'),
    path('pay/', views.payment, name='pay'),


 
    path('userhome/questions', views.questions_view, name='questions'),

    path('addproduct/', views.add_product, name='add_product'),
    path('viewproduct/', views.view_product, name='view_product'),
    path('editproduct/', views.edit_product, name='edit_product'),
    
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('editproduct/<int:id>/', views.edit_product, name='edit_product'),
    path('search/', views.search_view, name='search_view'),

    path('product/', views.product_view, name='product_view'),

    path('community/product.html', views.product_view, name='product_html'),
    path('products/<str:subcategory>/', views.products_by_subcategory, name='products_by_subcategory'),
    path('product/<int:product_name>/', views.product_details, name='product_details'),

    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('userhome/community/', views.community, name='community'),
    path('userhome/post_fitness_update/', views.post_fitness_update, name='post_fitness_update'),
    path('userhome/post_transformation/', views.post_transformation, name='post_transformation'),
    path('userhome/post_recipe/', views.post_recipe, name='post_recipe'),
    path('userhome/community/product.html', views.product_view, name='product_html'),  
    path('community/', views.community, name='community'),
    path('communitydetails/', views.community_details_view, name='communitydetails'),



    

  

 
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
