from django.shortcuts import render,redirect,HttpResponse
from .models import CustomUser
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, "home.html")

def userhome(request):
    return render(request, "userhome.html")

def register(request):
    
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phoneno', None)
        password = request.POST.get('password', None)
        cpassword = request.POST.get('cpassword', None)
        # role = CustomUser.CUSTOMER
        if username and email and phone and password:
            if CustomUser.objects.filter(email=email).exists():
                messages.success(request,("Email is already registered."))
            elif CustomUser.objects.filter(username=username).exists():
                messages.success(request,("Username is already registered."))
            elif password!=cpassword:
                messages.success(request,("Password's Don't Match, Enter correct Password"))
            else:
                user = CustomUser(username=username, email=email, phone=phone)
                user.set_password(password)  # Set the password securely
                user.is_active=True
                user.save()
                # user_profile = UserProfile(user=user)
                # user_profile.save()
                # activateEmail(request, user, email)
                return redirect('/signin')  
            
    return render(request, 'register.html')



def signin(request):
    # if request.method =='POST':
    #     email = request.POST["email"]
    #     password = request.POST["password"]
    #     user = authenticate(request, email=email, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('/home')
    #     # else:
    #     #     return redirect('/signin')
    # else:
    #     return render(request, 'signin.html')

   
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
                auth_login(request,user)
                return redirect('userhome')
            else:
                messages.success(request,("Invalid credentials."))
        else:
            messages.success(request,("Please fill out all fields."))
    return render(request, 'signin.html')

        

def signout(request):  # Rename the function to 'logout_view'
    logout(request)
    return redirect('home')  # Replace 'home' with your actual URL name



def about(request):
    
    return render(request, 'about.html')
