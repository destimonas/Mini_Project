from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

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
