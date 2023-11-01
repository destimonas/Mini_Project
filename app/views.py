from django.shortcuts import render,redirect,HttpResponse
from .models import CustomUser, UserProfile1
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
                    return redirect('trainer')
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


        

def logout(request):  # Rename the function to 'logout_view'
    auth_logout(request)
    return redirect('home')
   # return redirect('home')  # Replace 'home' with your actual URL name



def about(request):
    
    return render(request, 'about')

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

def nutritiondetails(request):

    nutritions = CustomUser.objects.filter(is_nutritionist=True)
    
    context = {
        'nutritions': nutritions,
    }
    return render(request, 'nutritiondetails.html', context)

def trainerdetails(request):
    trainers = CustomUser.objects.filter(is_trainer=True)

    context = {
        'trainers': trainers,
    }
    return render(request, 'trainerdetails.html', context)


def usertrainer(request):
    # Your view logic here
    return render(request, 'usertrainer.html')

def usernutrition (request):
    
    return render(request, 'usernutrition.html')


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
from .models import Trainer  # Import your Trainer model
from django.contrib import messages

def trainerreg(request):
    if request.method == 'POST':
        full_name = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        specialization = request.POST['specialization']
        phone_number = request.POST['phoneno']
        gender = request.POST['gender']

        # Create a new Trainer object and save it to the database
        trainer = Trainer(
            full_name=full_name,
            username=username,
            email=email,
            password=password,
            specialization=specialization,
            phone_number=phone_number,
            gender=gender
        )
        trainer.save()

        messages.success(request, "Registered Successfully")
        
        # Redirect to a different URL after registration (change 'some_url_name' to your desired URL)
        return redirect('/signin')
    
    # Render the 'trainerreg.html' template for GET requests
    return render(request, 'trainerreg.html')

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
        
        messages.success(request, "Registered Successfully")
        return redirect('/signin')

    return render(request, "nutritionreg.html")

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile1
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
