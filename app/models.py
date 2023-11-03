from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser,User
from django.conf import settings

from django.core.validators import RegexValidator

# Create your models here.

class CustomUser(AbstractUser):
    ADMIN=1
    TRAINER=2
    NUTRITIONIST=3
    USER=4

    USER_TYPES = (
        (ADMIN, 'Admin'),
        (TRAINER, 'Trainer'),
        (NUTRITIONIST, 'Nutritionist'),
        (USER, 'User'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, blank=True, null=True)
    
    username=models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    password = models.CharField(max_length=128)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_trainer = models.BooleanField(default=False)
    is_nutritionist = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)


    def _str_(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class UserProfile1(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    district= models.CharField(max_length=255, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)

    def __str__(self):
        return self.user.username



class FitnessGoal(models.Model):
    goal_type = models.CharField(max_length=255)
    goal_description = models.TextField()
    goal_deadline = models.DateField()
    duration = models.PositiveIntegerField(default=0)  # You can update this field as needed
    calories_burned = models.PositiveIntegerField(default=0)  # You can update this field as needed
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.goal_description
    

class Trainer(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    approved=models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name




class Nutritionist(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^[6789]\d{9}$', 'Invalid phone number.')])
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    def __str__(self):
        return self.full_name




class Specialization(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name
