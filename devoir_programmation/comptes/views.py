
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
#importing as such so that it doesn't create a confusion with our methods and django's default methods

from django.contrib.auth.decorators import login_required
from .forms import FormAuthentication, RegistrationForm
from .models import Compte
def index(request):
    return render(request,'index.html')

def login_comp(request):
    user = request.user
    if user.is_authenticated:
        return redirect("index")
    if request.method == 'POST':
        form = FormAuthentication(request.POST)
        email   = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                messages.success(request, "Logged In")
                return redirect('index') 
            else:
                messages.error("please Correct Below Errors")
    else:
        form = FormAuthentication()
    return render(request,'accounts/login.html',{'form':form,})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data = request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password1']
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            u = authenticate(request,email=email,password=password)
            login(request,u)
            return redirect('index')
    else:
        form = RegistrationForm()

    return render(request,'register.html',{'form':form})

def logout_cmp(request):
    logout(request)
    return redirect('/')

"""@login_required(login_url ="/")
def dashboard(request):
    return render(request, 'dashboard.html',{})"""