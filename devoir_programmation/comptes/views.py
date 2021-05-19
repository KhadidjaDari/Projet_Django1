
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import login as django_login, logout as django_logout, authenticate as django_authenticate
#importing as such so that it doesn't create a confusion with our methods and django's default methods

from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm, RegistrationForm
from .models import Compte

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = django_authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request,user)
                    return redirect('/dashboard') #user is redirected to dashboard
    else:
        form = AuthenticationForm()

    return render(request,'accounts/login.html',{'form':form,})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data = request.POST)
        if form.is_valid():
            index=None
            page=request.get_full_path()
            if page == '/reg':
                index=0
            else :
                index=1
            #user = form.save()
            user=Compte(username=request.POST['username'],email=request.POST['email'],password=request.POST['password1'],type_cmp=index).save()
            u = django_authenticate(email=request.POST['email'], password=request.POST['password1'])
            django_login(request,u)
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request,'register.html',{'form':form})

def logout(request):
    django_logout(request)
    return redirect('/')

"""@login_required(login_url ="/")
def dashboard(request):
    return render(request, 'dashboard.html',{})"""