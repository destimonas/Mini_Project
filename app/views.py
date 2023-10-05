from django.shortcuts import render,redirect,HttpResponse
from .models import CustomUser
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.


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
                messages.success(request,("Username is already registered."))
            elif CustomUser.objects.filter(email=email).exists():
                messages.success(request,("Email is already registered."))
            elif password!=cpassword:
                messages.success(request,("Password's don't Match, Enter correct Password"))
            else:

                user = CustomUser(username=username, email=email, phone=phone)
                user.set_password(password)  # Set the password securely
                user.is_active=True
                user.is_user=True
                user.save()
                # user_profile = UserProfile(user=user)
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
        # if user is not None:
        #     auth_login(request, user)
        #     return redirect('/userhome')
        # else:
        #    messages.success(request,("Invalid credentials."))
        # print(username)  # Print the email for debugging
        # print(password)  # Print the password for debugging

        if username and password:
            user = authenticate(request, username =username , password=password)
            
            if user is not None:
                 
                auth_login(request, user)
                request.session['username']=username
               
            
                # Redirect based on user_type
                if user.is_admin==True:
                    return redirect('http://127.0.0.1:8000/admin/login/?next=/admin/')
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


        

def signout(request):  # Rename the function to 'logout_view'
    auth_logout(request)
    return redirect('home')
   # return redirect('home')  # Replace 'home' with your actual URL name



def about(request):
    
    return render(request, 'about.html')


