import json
from django.shortcuts import render,redirect,HttpResponse

from .models import *
from django.contrib.auth import authenticate ,login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.http import JsonResponse
from .models import FitnessGoal
from django.template.loader import render_to_string


# Create your views here.


def admin_dashboard(request):
    # Add your code to render the admin dashboard here
    return render(request, 'adminpanel.html')


def home(request):
    return render(request, "home.html")

def userhome(request):
     if 'username' in request.session:
        response = render(request, 'userhome.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
     else:
         return redirect('home') 

def register(request):
    
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phoneno', None)
        password = request.POST.get('password', None)
        cpassword = request.POST.get('cpassword', None)
        # role = CustomUser.CUSTOMER
        if username and email and phone and password:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request,("Username is already registered."))
                redirect_url = reverse('register')  # Use the name of your registration view
                return redirect(redirect_url)
            elif CustomUser.objects.filter(email=email).exists():
                messages.error(request,("Email is already registered."))
                redirect_url = reverse('register')  # Use the name of your registration view
                return redirect(redirect_url)
            elif password!=cpassword:
                messages.error(request,("Password's don't Match,Enter correct Password"))
                redirect_url = reverse('register')  # Use the name of your registration view
                return redirect(redirect_url)
            else:

                user = CustomUser(username=username, email=email, phone=phone)
                user.set_password(password)  # Set the password securely
                user.is_active=True
                user.is_user=True
                user.save()
                # user_profile = Userprofile(user=user)
                # user_profile.save()
                # activateEmail(request, user, email)
                
                subject = 'Registration Confirmation'
                message = f'Hello {username},\n\nThank you for registering. Your username is: {username}\nYour password is: {password}\n\nYou can now log in.'
                from_email = 'destimonas2024a@mca.ajce.in'  # Use the same email you configured in settings.py
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                user_registered=True
                messages.success(request,("Registered Successfully"))
                
            return redirect('/signin') 

        
    return render(request, 'register.html', locals())

from django.shortcuts import render


def trainerhome(request):
    # Check if the user is authenticated and a trainer
    if request.user.is_authenticated and request.user.is_trainer:
        trainer = request.user  # Assuming request.user is the trainer
        context = {'trainer': trainer}
        return render(request, 'trainerhome.html', context)
    else:
        return redirect('signin')  # Redirect to login if not authenticated or not a trainer

# views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile1  # Adjust the import based on your models
from django.http import HttpResponse

class TrainerProfileView(LoginRequiredMixin, View):
    template_name = 'trainerprofile.html'

    def get(self, request):
        # Your existing GET logic
        # Assuming you have a TrainerProfile model, adjust accordingly
        trainer_profile, created = UserProfile1.objects.get_or_create(user=request.user)
        # Pass the trainer_profile to the template
        context = {
            'trainer_profile': trainer_profile,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        fullname = request.POST.get('fname')
        
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        state = request.POST.get('state')
        district = request.POST.get('district')
        age = request.POST.get('age')

        # Check if a TrainerProfile instance already exists for the user
        # Adjust the model name to match your TrainerProfile model
        trainer_profile, created = UserProfile1.objects.get_or_create(user=user)

        # Update the fields with the new data
        trainer_profile.fullname = fullname
      
        trainer_profile.phone = phone
        trainer_profile.gender = gender
        trainer_profile.state = state
        trainer_profile.district = district
        trainer_profile.age = age

        # Save the changes to the trainer profile
        trainer_profile.save()

        return redirect('trainerprofile')
    




def nutritionprofile(request):
    # Your view logic here
    return render(request, 'nutritionprofile.html')

def save_user_profile(request):
    # Your view logic here
    return HttpResponse("Save User Profile View")

def signin(request):
   
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = authenticate(request, username =username , password=password)
            
            if user is not None:
                 
                auth_login(request, user)
                request.session['username']=username
               
            
                # Redirect based on user_type
                if user.is_admin==True:
                    return redirect('/adminpanel')
                elif user.is_trainer==True:
                    print('trainer')
                    return redirect('/trainerhome')
                elif user.is_nutritionist==True:
                    return redirect('nutritionist')
                elif user.is_user==True:
                    return redirect('userhome')
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Please fill out all fields.")
            return redirect('signin')
    response = render(request,'signin.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response


        
from django.contrib.auth import authenticate,logout
def logout_user(request):  # Rename the function to 'logout_view'
    logout(request)
    return redirect('home')
   # return redirect('home')  # Replace 'home' with your actual URL name



def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')


def goal_setting_view(request):
    # Add your view logic here
    return render(request, 'goalsetting.html')

def user_goal_setting_view(request):

    return render(request, 'goalsetting.html')


def dashboardbase(request):

    return render(request, 'dashboardbase.html')

def userdetails(request):
    users = CustomUser.objects.filter(is_user=True)
    
    context = {
        'users': users,
    }
    return render(request, 'userdetails.html', context)

from .models import Nutritionist

def nutritiondetails(request):
    nutritions = Nutritionist.objects.all()  # Query the Nutritionist model

    context = {
        'nutritions': nutritions,
    }
    return render(request, 'nutritiondetails.html', context)




def trainerdetails(request):
    trainers = Trainer.objects.all()  # Query the Trainer model

    context = {
        'trainers': trainers,
    }
    return render(request, 'trainerdetails.html', context)




def usernutrition (request):
    
    return render(request, 'usernutrition.html')

def nutritionist (request):
    
    return render(request, 'nutritionist.html')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

# @require_POST
# @csrf_exempt
# def deactivate_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     user.is_active = False
#     user.save()
#     return redirect('userdetails')
  

# @require_POST
# @csrf_exempt
# def activate_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     user.is_active = True
#     user.save()
#     return redirect('userdetails')
    

def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()

        # Send activation email
        subject = 'Account Activation'
        message = 'Your account has been activated by the admin.'
        from_email = 'destimonas2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been activated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('userdetails')

def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'destimonas2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_email.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already deactivated.")
    return redirect('userdetails')




def classess(request):
    
    return render(request, "classess.html")

def content(request):
    
    return render(request, "content.html")

from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.hashers import make_password
def trainerreg(request):
    if request.method == 'POST':
        full_name = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        specialization_id = request.POST['specialization']  # Assuming 'specialization' is an id
        phone_number = request.POST['phoneno']
        gender = request.POST['gender']
        certificate1 = request.FILES['certificate']
        govt_id = request.FILES['govt_id']

        # Fetch the Specialization instance
        specialization_instance = Specialization.objects.get(pk=specialization_id)

        # Create a new Trainer object and save it to the database
        trainer = Trainer(
            full_name=full_name,
            username=username,
            email=email,
            specialization=specialization_instance,  # Assign the instance, not the id
            phone_number=phone_number,
            gender=gender,
            certificate=certificate1,
            govt_id=govt_id,
        )
        trainer.password = make_password(password)
        trainer.save()

        details = CustomUser(
            username=username,
            email=email,
            is_trainer=True
        )
        details.set_password(password)
        details.save()

        messages.success(request, "Registered Successfully")

        # Redirect to a different URL after registration (change 'some_url_name' to your desired URL)
        return redirect('/signin')

    specialization = Specialization.objects.all()
    return render(request, 'trainerreg.html', {'specialization': specialization})


from .models import Nutritionist

def nutritionreg(request):
    if request.method == 'POST':
        full_name = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        specialization = request.POST['specialization']
        phone_number = request.POST['phoneno']
        gender = request.POST['gender']

        # Create a new Nutritionist object and save it to the database
        nutritionist = Nutritionist(
            full_name=full_name,
            username=username,
            email=email,
            password=password,
            specialization=specialization,
            phone_number=phone_number,
            gender=gender
        )
        nutritionist.save()
        details=CustomUser(username=username,
            email=email,
            password=password,
            is_nutritionist=True)
        details.save()
        
        messages.success(request, "Registered Successfully")
        return redirect('/signin')
    
    # specialization = Specialization.objects.all()
    # return render(request, 'trainerreg.html', {'specialization': specialization})

    return render(request, "nutritionreg.html")

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserProfile1  # Import your model

class UserProfileCreateView(LoginRequiredMixin, View):
    template_name = 'userprofile.html'

    def get(self, request):
        # Your existing GET logic
        user_profile, created = UserProfile1.objects.get_or_create(user=request.user)

        # Pass the user_profile to the template
        context = {
            'user_profile': user_profile,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        fullname1 = request.POST.get('fname')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        state = request.POST.get('state')
        district = request.POST.get('district')
        age = request.POST.get('age')

        # Check if a UserProfile1 instance already exists for the user
        user_profile, created = UserProfile1.objects.get_or_create(user=user)

        # Update the fields with the new data
        user_profile.fullname = fullname1
        user_profile.height = height
        user_profile.weight = weight
        user_profile.phone = phone
        user_profile.gender = gender
        user_profile.state = state
        user_profile.district = district
        user_profile.age = age

        # Save the changes to the user profile
        user_profile.save()

        return redirect('userprofile')


def update_specialization(request, pk):
    specialization_instance = get_object_or_404(Specialization, pk=pk)
    
    if request.method == 'POST':
        # Update the specialization with the new data
        new_specialization = request.POST.get("specialization")
        new_description = request.POST.get("description")
        specialization_instance.name = new_specialization
        specialization_instance.description = new_description
        specialization_instance.save()
        
        return redirect('specialization_list')
    
    return render(request, 'update_specialization.html', {'specialization': specialization_instance})




from django.shortcuts import render, redirect
from .models import FitnessGoal

def save_fitness_goal(request):
    if request.method == 'POST':
        goal_type = request.POST.get('goal-type')
        goal_description = request.POST.get('goal-description')
        goal_deadline = request.POST.get('goal-deadline')

        # Create a new FitnessGoal instance and save it to the database
        fitness_goal = FitnessGoal(
            goal_type=goal_type,
            goal_description=goal_description,
            goal_deadline=goal_deadline,
        )
        fitness_goal.save()

        # You can also calculate and set 'duration' and 'calories_burned' fields here

    return redirect('goalsetting')  # Redirect to the appropriate URL after submission
# views.py
from django.shortcuts import render
from .models import FitnessGoal

def display_goals(request):
    goals = FitnessGoal.objects.all()
    return render(request, 'goalsetting.html', {'goals': goals})


# def specialization(request):
#     return render(request, "specialization.html")

def specialization_list(request):
    specializations = Specialization.objects.all()
    return render(request, 'specialization.html', {'specializations': specializations})

def create_specialization(request):
    if request.method == 'POST':
        name = request.POST.get('specialization')
        description = request.POST.get('description')
        
        # Check if a specialization with the same name already exists
        if Specialization.objects.filter(name=name).exists():
            messages.error(request, f'Specialization with name "{name}" already exists.')
        else:
            Specialization.objects.create(name=name, description=description)
            return redirect('specialization_list')

    return redirect('specialization_list')

from django.shortcuts import render, redirect, get_object_or_404
# from .models import Specialization
from django.shortcuts import render, redirect, get_object_or_404


def delete_specialization(request, pk):
    specialization_instance = get_object_or_404(Specialization, pk=pk)
    
    if request.method == 'POST':
        specialization_instance.delete()
        return redirect('specialization_list')
    
    return render(request, 'confirm_delete_specialization.html', {'specialization': specialization_instance})

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')  # Get the old password from the form
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user  # Get the currently logged-in user

        # Check if the entered old password matches the user's current password
        if not user.check_password(old_password):
            return JsonResponse({'error': 'Incorrect old password'}, status=400)

        if new_password == confirm_password:
            # Change the user's password and save it to the database
            user.set_password(new_password)
            user.save()

            # Update the session to keep the user logged in
            update_session_auth_hash(request, user)

            return JsonResponse({'message': 'Password changed successfully'})
        else:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

    return render(request, 'change_password.html')

from django.http import HttpResponseRedirect
# views.py



def approve_trainer(request, trainer_id):
    trainer = Trainer.objects.get(pk=trainer_id)
    # Perform the approval logic (e.g., setting trainer.approved = True)
    trainer.approved = True
    trainer.save()
    # Send an email to the registered email
    subject = 'Approval Notification'
    message = 'You have been approved as a trainer.'
    from_email = 'destimonas2024a@mca.ajce.in'
    recipient_list = [trainer.email]
    send_mail(subject, message, from_email, recipient_list)

    return HttpResponseRedirect(reverse('trainerdetails'))

# View to approve a Nutritionist
def approve_nutritionist(request, nutritionist_id):
    nutritionist = Nutritionist.objects.get(pk=nutritionist_id)
    nutritionist.approved = True
    nutritionist.save()

    # Send an email to the registered email
    subject = 'Approval Notification'
    message = 'You have been approved as a nutritionist.'
    from_email = 'destimonas2024a@mca.ajce.in'
    recipient_list = [nutritionist.email]
    send_mail(subject, message, from_email, recipient_list)
    
    return HttpResponseRedirect(reverse('nutritiondetails'))

def reject_trainer(request, trainer_id):
    trainer = Trainer.objects.get(pk=trainer_id)
    # Perform the rejection logic (e.g., setting trainer.approved = False)
    trainer.approved = False
    trainer.save()
    # Send an email to the registered email
    subject = 'Rejection Notification'
    message = 'You have been rejected as a trainer.'
    from_email = 'destimonas2024a@mca.ajce.in'
    recipient_list = [trainer.email]
    send_mail(subject, message, from_email, recipient_list)

    return HttpResponseRedirect(reverse('trainerdetails'))


# View to reject a Nutritionist
def reject_nutritionist(request, nutritionist_id):
    nutritionist = Nutritionist.objects.get(pk=nutritionist_id)
    nutritionist.approved = False
    nutritionist.save()

    # Send an email to the registered email
    subject = 'Rejection Notification'
    message = 'You have been rejected as a nutritionist.'
    from_email = 'destimonas2024a@mca.ajce.in'
    recipient_list = [nutritionist.email]
    send_mail(subject, message, from_email, recipient_list)
    
    return HttpResponseRedirect(reverse('nutritiondetails'))




def usertrainer(request):
    trainers = Trainer.objects.all() 
   
    return render(request, 'usertrainer.html', {'trainers': trainers})

from .models import Payment

def payment(request):
    if request.method == 'POST':
        # Assuming you have a form that captures customer details
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_contact = request.POST.get('customer_contact')
        amount = 100  # You may adjust this based on your logic

        try:
            payment = Payment.objects.create(
                amount=amount,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_contact=customer_contact
            )
            print(f"Payment successful: {payment}")
        except Exception as e:
            print(f"Error saving payment: {e}")
            return HttpResponse("Error saving payment. Please try again.")

        # Pass the payment ID to the Razorpay checkout.js script
        context = {
            'payment_id': payment.id,
            'razorpay_key': 'rzp_test_v4Tz9K1hhXrTYr',  # Your Razorpay API key
        }
        return redirect('usertrainer')

    return HttpResponse("Method not allowed")

def consult_trainer(request):
    if request.method == 'POST':
        # Handle the consultation logic here
        trainer_id = request.POST.get('trainer_id')
        # You can add your consultation logic here
        return HttpResponse('Consultation successful')
    else:
        # Handle GET request for consultation
        return HttpResponse('Invalid request')

def usernutrition(request):
    
    nutritionists = Nutritionist.objects.all()
    return render(request, 'usernutrition.html', {'nutritionists': nutritionists})



def weekly_class_schedule(request):
    # Define your schedule data here or fetch it from a database.
    # For simplicity, we'll use static data in this example.
    schedule_data = [
        {
            'day': 'Sunday',
            'event': 'Yoga Class',
            'time': '10:00 AM - 11:30 AM',
          
        },
        {
            'day': 'Sunday',
            'event': 'Zumba Class',
            'time': '3:00 PM - 4:30 PM',
       
        },
        {
            'day': 'Monday',
            'event': 'Pilates Class',
            'time': '9:30 AM - 11:00 AM',
         
        },
        {
            'day': 'Monday',
            'event': 'Spinning Class',
            'time': '1:00 PM - 2:30 PM',
        
        },
        {
            'day': 'Monday',
            'event': 'Aerobics Class',
            'time': '6:00 PM - 7:30 PM',
         
        },
        # Add more schedule data for other days and events as needed.
    ]

    return render(request, 'schedule.html', {'schedule_data': schedule_data})

def rate_trainer(request, trainer_id):
    if request.user.is_authenticated:
        
        if request.method == 'POST':
            user = request.user  # Assuming you have authentication set up
            trainer = Trainer.objects.get(id=trainer_id)
            rating = request.POST['rating']
            feedback = request.POST['feedback']
            user_rating = UserRating(user=user, trainer=trainer, rating=rating, feedback=feedback)
            user_rating.save()
            return redirect('usertrainer')
    trainers = Trainer.objects.all()
    trainer = get_object_or_404(Trainer, pk=trainer_id)

    context = {
        'trainer': trainer,
        'trainers': trainers,
    }
    return render(request, 'rating.html', context)
from django.contrib.auth.decorators import login_required

@login_required
def add_slot(request):
    # Fetch the Trainer instance associated with the current user outside of the if block
    try:
        trainer = Trainer.objects.get(username=request.user)
    except Trainer.DoesNotExist:
        messages.error(request, 'Trainer information not found for the current user.')
        return redirect('trainerhome')  # Redirect to an appropriate page
    print("Trainer instance:", trainer)  # Add this line for debugging

    if request.method == "POST":
        session = request.POST.get('session')
        time = request.POST.get('time')

        # Check if the time slot already exists for the current trainer
        if TimeSlot.objects.filter(session=session, time=time, trainer=trainer).exists():
            messages.error(request, 'This time slot already exists.')
        else:
            TimeSlot.objects.create(session=session, time=time, trainer=trainer)
            messages.success(request, 'Slot added successfully.') 
    slots = TimeSlot.objects.filter(trainer=trainer)
    context = {
        "slots": slots,
        "trainer": trainer
    }
    return render(request, 'addslot.html', context)

from django.shortcuts import render


def trainer_list(request):
    # Fetch all available slots for the current trainer
    trainer_slots = TimeSlot.objects.filter(trainer=request.user)

    # Create a dictionary to store the counts for each session
    session_counts = {
        'morning': 0,
        'afternoon': 0,
        'evening': 0,
    }

    # Count the slots for each session
    for slot in trainer_slots:
        session_counts[slot.session] += 1

    context = {
        'session_counts': session_counts,
        'slots': trainer_slots,  # Include all the slots in the context
        # Other context data
    }

    return render(request, 'userhome.html', context)


def questions_view(request):
  
    return render(request, 'questions.html') 


def add_product(request):
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        category, created = Category1.objects.get_or_create(name=category_name)

        # Retrieve or create the Subcategory2 instance while providing the Category2 instance
        subcategory_name = request.POST.get('subcategory-name')
        subcategory, created = Subcategory1.objects.get_or_create(name=subcategory_name, category=category)

        # Handle the form submission
        product_name = request.POST.get('product-name')
        stock = request.POST.get('stock')  # Retrieve quantity from the form
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        status = request.POST.get('status')
        product_image = request.FILES.get('product-image')

        price = float(price)
        discount = float(discount)

        # Calculate sale_price
        sale_price = price - (price * (discount / 100))

        # Create a new Product2 object and save it to the database
        product = Product1(
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            stock=stock,  # Assign the quantity field
            description=description,
            price=price,
            discount=discount,
            sale_price=sale_price,
            status=status,
            product_image=product_image,
        )
        product.save()

        # Redirect to a success page or any other desired action
        return redirect('dashboardbase')

    return render(request, 'addproduct.html')


def view_product(request):
    products = Product1.objects.all()  # Retrieve all products from the database
    return render(request, 'viewproduct.html', {'products': products})

def delete_product(request, product_id):
    if request.method == 'POST':
        # Delete the product from the database
        try:
            product = Product1.objects.get(pk=product_id)
            product.delete()
        
        except Product1.DoesNotExist:
            pass
    return redirect('view_product')  # Redirect back to the product list view

def edit_product(request, id):
    # Retrieve the product using get_object_or_404 to handle cases where the product doesn't exist
    product = get_object_or_404(Product1, pk=id)

    if request.method == 'POST':
       
        product.product_name = request.POST['product-name']
        product.category1 = request.POST['category-name']
        product.subcategory1 = request.POST['subcategory-name']
        product.stock = request.POST['stock']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.discount = request.POST['discount']
        product.sale_price = request.POST['sale-price']
     
        
        # Save the updated product
        product.save()

        # Redirect to a product detail page or a success page
        #return HttpResponseRedirect('/product_detail/{0}/'.format(product.product_id))
       # return HttpResponseRedirect('adminpanel')

    # If the request method is GET, render the edit product form
    return render(request, 'editproduct.html', {'product': product})

def search_view(request):
    query = request.GET.get('q')
    if query:
        # Perform the search operation based on the query
        products = Product1.objects.filter(product_name__icontains=query)
    else:
        # If no query is provided, return all products
        products = Product1.objects.all()

    return render(request, 'viewproduct.html', {'products': products, 'query': query})




def product_view(request):
    # Retrieve all products from the database
    products = Product1.objects.all()
    return render(request, 'product.html', {'products': products})
    

def products_by_subcategory(request, subcategory):
    # Retrieve the subcategory object based on its name
    subcategory = get_object_or_404(Subcategory1, name=subcategory)
    
    # Query products based on the retrieved subcategory object
    products = Product1.objects.filter(subcategory=subcategory)
    
    return render(request, 'product.html', {'products': products})


@login_required
def product_details(request, product_id):
    # Retrieve the product
    product = get_object_or_404(Product1, pk=product_id)

    # Fetch all ratings for the current product
    ratings = Productrating.objects.filter(product=product)

    # Pass product and ratings to the template context
    return render(request, 'productdetails.html', {'product': product, 'ratings': ratings})


def add_to_cart(request, id):
    product = Product1.objects.get(pk=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')

def remove_from_cart(request, id):
    product = Product1.objects.get(pk=id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
             cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('view_cart')

@login_required(login_url='login')
def increase_cart_item(request, id):
    product = Product1.objects.get(pk=id)
    cart = request.user.cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if cart_item.quantity < product.stock:
     cart_item.quantity += 1
     cart_item.save()

    return redirect('view_cart')

@login_required(login_url='login')
def decrease_cart_item(request, id):
    product = Product1.objects.get(pk=id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')


def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.total_price = item.product.sale_price * item.quantity
    
    total_amount = sum(item.total_price for item in cart_items)

    return render(request, 'view_cart.html', {'cart_items': cart_items,'total_amount': total_amount})

def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count


def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.total_price = item.product.sale_price * item.quantity
    
    total_amount = sum(item.total_price for item in cart_items)

    return render(request, 'view_cart.html', {'cart_items': cart_items,'total_amount': total_amount})

    
from django.shortcuts import render, redirect
from .models import Discussion

@login_required
def community(request):
    discussions = Discussion.objects.all()
    

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        if title and content:
            # Ensure the user is authenticated and is an instance of CustomUser
            if isinstance(request.user, CustomUser):
                user = request.user  
                discussion = Discussion.objects.create(
                    title=title,
                    content=content,
                    image=image,
                    user=user
                )
                messages.success(request, 'Discussion post added successfully')
                return redirect('community')
            else:
                messages.error(request, 'User is not authenticated or is not a CustomUser instance.')
                return redirect('login')  # Redirect to login page if user is not authenticated
        else:
            messages.error(request, 'Title and content cannot be empty.')
            return redirect('community')  # Redirect back to the community page
    return render(request, 'community.html', {'discussions': discussions})



@login_required
def post_fitness_update(request):
    if request.method == 'POST':
        content = request.POST.get('fitnessUpdateContent')
        image = request.FILES.get('fileInputFitnessUpdate')

        if content:  # Check if content is not empty
            # Assuming you have a CustomUser model for authenticated users
            user = request.user
            fitness_update = FitnessUpdate.objects.create(
                content=content,
                image=image,
                user=user
            )
            messages.success(request, 'Fitness updates added successfully')  # Add success message
            return redirect('community')
        else:
            # Handle case where content is missing or empty
            messages.error(request, 'Content is required')  # Add error message
            return render(request, 'community.html', {'error_message': 'Content is required'})

    # Handle GET request or invalid form submission
    return render(request, 'community.html')
@login_required
def post_transformation(request):
    transformations = Transformation.objects.all()

    if request.method == 'POST':
        content = request.POST.get('transformationContent')
        image = request.FILES.get('fileInputTransformation')

        if content:  
            user = request.user
            transformation = Transformation.objects.create(
                content=content,
                image=image,
                user=user
            )
            messages.success(request, 'Successfully added transformation post')
            return redirect('community')
        else:
            messages.error(request, 'Content is required')
            return redirect('community')

    return render(request, 'community.html', {'transformations': transformations})

# @login_required
# def fetch_transformations(request):
#     transformations = Transformation.objects.all()
#     transformation_data = []

#     for transformation in transformations:
#         transformation_data.append({
#             'content': transformation.content,
#             'image': transformation.image.url if transformation.image else None,
#             'user': transformation.user.username
#         })

#     return JsonResponse(transformation_data, safe=False)
# Fetch transformations
@login_required
def fetch_transformations(request):
    transformations = Transformation.objects.all()
    transformation_data = []

    for transformation in transformations:
        transformation_data.append({
            'id': transformation.id,
            'content': transformation.content,
            'image': transformation.image.url if transformation.image else None,
            'user': transformation.user.username,
            'likes': transformation.likes.count(),
        })

    return JsonResponse(transformation_data, safe=False)



@login_required
def post_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('recipeName')
        story = request.POST.get('recipeStory')
        food_type = request.POST.get('foodType')
        cuisine_type = request.POST.get('cuisineType')
        cooking_time = request.POST.get('cookingTime')
        ingredients = request.POST.get('ingredients')
        directions = request.POST.get('directions')
        image = request.FILES.get('fileInputRecipe')

        if name and ingredients and directions:  # Check if essential fields are not empty
            # Assuming you have a CustomUser model for authenticated users
            user = request.user
            recipe = Recipe.objects.create(
                name=name,
                story=story,
                food_type=food_type,
                cuisine_type=cuisine_type,
                cooking_time=cooking_time,
                ingredients=ingredients,
                directions=directions,
                image=image,
                user=user
            )
            messages.success(request, 'Recipe post added successfully')  # Add success message
            return redirect('community')
        else:
            # Handle case where essential fields are missing or empty
            messages.error(request, 'Name, Ingredients, and Directions are required')  # Add error message
            # Redirect back to the recipe form page with an error message
            return redirect('community')

    # For GET request, fetch all recipes and render the community page
    recipes = Recipe.objects.all()
    return render(request, 'community.html', {'recipes': recipes})

def fetch_recipe(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        recipe_data = []
        for recipe in recipes:
            recipe_data.append({
                'name': recipe.name,
                'story': recipe.story,
                'food_type': recipe.food_type,
                'cuisine_type': recipe.cuisine_type,
                'cooking_time': recipe.cooking_time,
                'ingredients': recipe.ingredients,
                'directions': recipe.directions,
                'image_url': recipe.image.url if recipe.image else None,
                'posted_by': recipe.user.username
            })
        return JsonResponse(recipe_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

from django.views.decorators.http import require_POST
from django.http import JsonResponse

@require_POST
def post_comment(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    user = request.user
    content = request.POST.get('content')

    if content:
        # Create the comment object
        comment = Comment.objects.create(discussion=discussion, user=user, content=content)
        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Comment posted successfully.'})
    else:
        # Return error response if content is missing
        return JsonResponse({'status': 'error', 'message': 'Content is required.'})


def fetch_comments(request, discussion_id):
    discussion = Discussion.objects.get(pk=discussion_id)
    comments = discussion.comments.all()
    comment_data = []
    for comment in comments:
        comment_data.append({
            'user': comment.user.username,
            'content': comment.content
        })
    return JsonResponse(comment_data, safe=False)

@require_POST
def toggle_like(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    user = request.user

    if user in discussion.likes.all():
        # If the user already liked the discussion, unlike it
        discussion.likes.remove(user)
        liked = False
    else:
        # If the user hasn't liked the discussion yet, like it
        discussion.likes.add(user)
        liked = True

    like_count = discussion.likes.count()  # Get the total number of likes for the discussion

    return JsonResponse({'status': 'success', 'like_count': like_count})


# Toggle like for a transformation
@login_required
@require_POST
def toggle_transformation_like(request, transformation_id):
    transformation = get_object_or_404(Transformation, pk=transformation_id)
    user = request.user

    if user in transformation.likes.all():
        transformation.likes.remove(user)
        liked = False
    else:
        transformation.likes.add(user)
        liked = True

    like_count = transformation.likes.count()

    return JsonResponse({'status': 'success'})

# Post a comment for a transformation
@login_required
@require_POST
def post_transformation_comment(request, transformation_id):
    transformation = get_object_or_404(Transformation, pk=transformation_id)
    user = request.user
    content = request.POST.get('content')

    if content:
        comment = Comment.objects.create(transformation=transformation, user=user, content=content)
        return JsonResponse({'status': 'success', 'message': 'Comment posted successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Content is required.'})

def fetch_transformation_comments(request, transformation_id):
    transformation_comments = Comment.objects.filter(transformation_id=transformation_id)
    comments_data = [{'user': comment.user.username, 'content': comment.content} for comment in transformation_comments]
    return JsonResponse(comments_data, safe=False)


from django.shortcuts import render
from .models import FitnessCenter  # Import your FitnessCenter model

def explore(request):
    # Fetch fitness centers from the database
    fitness_centers = FitnessCenter.objects.all()
    return render(request, 'explore.html', {'fitness_centers': fitness_centers})


def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = Product1.objects.get(id=product_id)
        wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
        # if created:
        #     # The item was added to the wishlist
        #     messages.success(request, f'{product.product_name} has been added to your wishlist.')
        # else:
        #     # The item is already in the wishlist
        #     messages.warning(request, f'{product.product_name} is already in your wishlist.')
    return redirect('wishlist')



def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('product_view') 

def remove_from_wishlist(request, product_id):
    if request.user.is_authenticated:
        # Get the wishlist item or return a 404 if it doesn't exist
        wishlist_item = get_object_or_404(WishlistItem, user=request.user, product_id=product_id)
        
        # Delete the wishlist item
        wishlist_item.delete()
        
        # Display a success message
        # messages.success(request, f'Item removed from your wishlist.')

    return redirect('wishlist') 


# views.py
from .models import FitnessCenter

def add_fitness_center(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        latitude_str = request.POST.get('latitude')
        longitude_str = request.POST.get('longitude')
        address = request.POST.get('address')
        
        # Create a new FitnessCenter object and save it to the database

        # Create a new FitnessCenter object and save it
        fitness_center = FitnessCenter.objects.create(
            name=name,
            latitude=latitude_str,
            longitude=longitude_str,
            address=address
        )
        fitness_center.save()

        return redirect('dashboardbase')
    return render(request, 'add_fitness_center.html')



@login_required
def rate_product(request, product_id):
    if request.method == 'POST':
        # Retrieve the product
        product = get_object_or_404(Product1, pk=product_id)

        # Get rating and comment from the form submission
        rating_value = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        # Create a new product rating object
        product_rating = Productrating.objects.create(
            user=request.user,
            product=product,
            value=rating_value,
            comment=comment
        )

        # Fetch all ratings for the current product
        ratings = Productrating.objects.filter(product=product)

        # Render the template with the updated ratings
        return render(request, 'productdetails', {'ratings': ratings})
    else:
        # Handle GET requests if needed
        pass

@login_required  
def checkout(request):
    user_profile = UserProfile1.objects.filter(user=request.user).first()

    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    cart_count = get_cart_count(request)

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'user_profile': user_profile,
    }
    return render(request, 'checkout.html', context)

def edit_address(request):
    if request.method == 'POST':
        # Assuming you have a UserProfile1 model with fields 'address' and 'pincode'
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')

        # Retrieve the user's profile
        user_profile = UserProfile1.objects.filter(user=request.user).first()

        # Update the address and pincode fields
        if user_profile:
            user_profile.address = address
            user_profile.pincode = pincode
            user_profile.save()

        # Redirect to the checkout page after editing the address
        return redirect('checkout')

    # If the request method is not POST, simply redirect to the checkout page
    return redirect('checkout')

def handle_payment(request):
    if request.method == 'POST':
        # Retrieve the payment details from the POST request
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        # Perform signature verification
        # Your code for verifying the signature goes here

        # If signature is verified, mark the payment as successful
        # Your code for updating the order status and processing the payment goes here

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failure'})


