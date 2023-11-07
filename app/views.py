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

def trainer_home(request):
    # You can add additional logic here to customize the trainer's dashboard content
    return render(request, 'trainerhome.html')

def trainerprofile(request):
    # Your view logic here
    return render(request, 'trainerprofile.html')


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

from .models import Nutritionist

def nutritiondetails(request):
    nutritions = Nutritionist.objects.all()  # Query the Nutritionist model

    context = {
        'nutritions': nutritions,
    }
    return render(request, 'nutritiondetails.html', context)


from .models import Trainer  # Import the Trainer model

def trainerdetails(request):
    trainers = Trainer.objects.all()  # Query the Trainer model

    context = {
        'trainers': trainers,
    }
    return render(request, 'trainerdetails.html', context)


def usertrainer(request):
    # Your view logic here
    return render(request, 'usertrainer.html')

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
        details=CustomUser(username=username,
            email=email,
            password=password,
            is_trainer=True)
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



def add_slot(request):
    if request.method == "POST":
        session = request.POST.get("session")
        time = request.POST.get("time")
        TimeSlot.objects.create(session=session, time=time)
        return redirect("add_slot")  # Redirect back to the form after submission

    slots = TimeSlot.objects.all()
    return render(request, 'addslot.html', {"slots": slots})
