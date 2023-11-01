from django.contrib import admin
from .models import CustomUser, UserProfile1,FitnessGoal
# Register your models here.
admin.site.register(CustomUser)


admin.site.register(UserProfile1)
admin.site.register(FitnessGoal)

