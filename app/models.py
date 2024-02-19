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
    
class Specialization(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Trainer(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=100)
    specialization = models.ForeignKey('Specialization', on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    approved=models.BooleanField(default=False)
    # time_slots = models.ManyToManyField('TimeSlot', related_name='trainers')

    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)  # FileField for certificate uploads
    govt_id = models.FileField(upload_to='govt_ids/', blank=True, null=True)  # FileField for government ID uploads
    
    def __str__(self):
        return self.full_name


class TimeSlot(models.Model):
    session_choices = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]
    session = models.CharField(max_length=20, choices=session_choices)
    time = models.CharField(max_length=50)
    
    # Add a ForeignKey field to establish a relationship with the Trainer model
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='time_slots')

    def __str__(self):
        return f"{self.session} - {self.time} ({self.trainer.full_name})"


class UserRating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Assuming you have a User model
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, blank=True, null=True)

    rating = models.PositiveIntegerField()
    feedback = models.TextField()
    date_rated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user.username} rated {self.trainer.full_name} - {self.rating} stars'



class Nutritionist(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    specialization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^[6789]\d{9}$', 'Invalid phone number.')])
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    approved=models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name
    
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_contact = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.customer_name} - {self.amount}"
    
class Category1(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Subcategory1(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
   

class Product1(models.Model):
    
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category1, on_delete=models.CASCADE)  # Use ForeignKey to relate to Category
    subcategory = models.ForeignKey(Subcategory1, on_delete=models.CASCADE)  # Use ForeignKey to relate to Subcategory
    stock = models.PositiveIntegerField(default=1, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    product_image = models.ImageField(upload_to='product_images/')
    STATUS_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]


    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Stock')

    def save(self, *args, **kwargs):
        # Update the status based on the quantity value
        if self.stock == 0:                                                                                                                                                                 
            self.status = 'Out of Stock'
        else:
            self.status = 'In Stock'

        # Convert self.discount to a float and then calculate the sale price
        self.discount = float(self.discount)  # Convert to float
        self.price = float(self.price)  # Convert to float
        self.sale_price = self.price - (self.price * (self.discount / 100))

        super(Product1, self).save(*args, **kwargs)


    def str(self):
        return self.product_name

class Discussion(models.Model):
    title = models.CharField(max_length=255,blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='discussion_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

# Model for Fitness Updates
class FitnessUpdate(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='fitness_updates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

# Model for Transformations
class Transformation(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='transformations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

# Model for Recipes
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    story = models.TextField()
    food_type = models.CharField(max_length=50)
    cuisine_type = models.CharField(max_length=50)
    cooking_time = models.CharField(max_length=50)
    ingredients = models.TextField()
    directions = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)








    
    


    




