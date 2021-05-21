
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login,logout
#importing as such so that it doesn't create a confusion with our methods and django's default methods

from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm, RegistrationForm
from .models import Compte
def index(request):
    return render(request,'index.html')
def login_comp(request):
    if request.method == 'POST':
        form = FormAuthentication(data = request.POST)
        if form.is_valid():
            email = request.POST['email']
            password =request.POST['password']
            user = authenticate(request,email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('index') #user is redirected to dashboard
    else:
        form = FormAuthentication()

    return render(request,'accounts/login.html',{'form':form,})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data = request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password1']
            index=None
            page=request.get_full_path()
            if page == '/reg':
                index=0
            else :
                index=1
            #user = form.save()
            user=Compte(username=request.POST['username'],email=request.POST['email'],password=request.POST['password1'],type_cmp=index).save()
            u = authenticate(request,email=email,password=password)
            login(request,u)
            return redirect('reg',{{'u',u}})
    else:
        form = RegistrationForm()

    return render(request,'register.html',{'form':form})

def logout_cmp(request):
    logout(request)
    return redirect('/')

"""@login_required(login_url ="/")
def dashboard(request):
    return render(request, 'dashboard.html',{})"""