from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
    return render(request, 'html/home.html')
    #return HttpResponse("hii i am ritik suthar")

def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        user_obj = User.objects.filter(username = username).first()
        print(user_obj)
        if user_obj is None:
            messages.success(request,'User not found')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user = user_obj).first()

        if not profile_obj.is_verfied:
            messages.success(request,'Profile is not verified chack your mail')
            return redirect('/login')

        user =  authenticate(username = username , password = password)
        if user is None:
            messages.success(request,'Wrong password')
            return redirect('/login')

        login(request, user)
        return redirect('/succes')


    return render(request, "html/login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request,"username is alredy taken")
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.success(request,"email is alredy taken")
                return redirect('/register')

            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            print(auth_token)
            profile_obj = Profile.objects.create(user= user_obj, auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, "html/register.html")

def success(request):
    return render(request, "html/succes.html")

def token_send(request):
    return render(request, 'html/token_send.html')

def send_mail_after_registration(email, token):
    subject = 'you account need to be verified'
    message = (f'hiii...paste the link to verify your account http://127.0.0.1:8000/verify/{token}')
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)

def verify(request, auth_token):
    try:
        Profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if Profile_obj:
            Profile_obj.is_verfied = True
            Profile_obj.save()
            messages.success(request, "your account is verified")
            return redirect('/login')
        else:
            return redirect("error")
    except Exception as e:
        print(e)

def error_page(request):
    return render(request, 'html/error.html')