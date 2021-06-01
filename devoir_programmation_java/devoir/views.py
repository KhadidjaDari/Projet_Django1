from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import template
from django.template import loader
from .forms import Ajouterdevoir
from .models import Enseignants
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
 return render(request,'home.html')
def AjouterDevoir(request):
    print("0000000000")
    user = request.user
    print("0000000000")
    if user.is_authenticated:
        print("0000000000")
        if request.method == 'POST':
            print("*******")
            form = Ajouterdevoir(data = request.POST)
            print("***************")
            if form.is_valid():
                form.save()
                return render(request,'dashboard.html',{})
        else:
            print("9999999999")
            form = Ajouterdevoir()
            print("9999999999")
            e=Enseignants.objects.get(user=user)
            print("9999999999")
        return render(request,'dashboard.html',{'form':form,'e':e})

@login_required()
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist :

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

