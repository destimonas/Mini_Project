from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username, phone, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone, 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email, password=None):
        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.user_type=1
        user.save(using=self._db)
        return user

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

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPES, default='4')
    username=models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=128)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    objects = UserManager()

    def _str_(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
