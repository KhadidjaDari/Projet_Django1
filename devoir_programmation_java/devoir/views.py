from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import template
from django.template import loader
from .forms import Ajouterdevoir
from .models import Enseignants,Devoirs,Categorie
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
            titre=request.POST['titre']
            fichier=request.FILES['fichier']
            print(fichier.name)
            type_dev=request.POST['type_dev']
            #date_dep=request.POST['date_dep']
            date_fin=request.POST['date_fin']
            module=request.POST['module']
            c=Categorie.objects.get(nom=module)
            e=Enseignants.objects.get(user=user)
            devoir=Devoirs(titre=titre,fichier=fichier,type_dev=type_dev,date_fin=date_fin,module=c,id_ens=e)
            devoir.save()
            return render(request,'dashboard.html',{})
        return render(request,'dashboard.html',{})

@login_required()
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        if load_template == 'dashboard.html':
            user = request.user
            c=Categorie.objects.all()      
            return render(request,'dashboard.html',{'c':c})

            
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist :

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

