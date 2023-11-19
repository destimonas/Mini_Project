from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)


admin.site.register(UserProfile1)
admin.site.register(FitnessGoal)
admin.site.register(Specialization)
admin.site.register(Trainer)
admin.site.register(UserRating)
admin.site.register(TimeSlot)


