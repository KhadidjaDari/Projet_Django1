from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import template
from django.template import loader
from .forms import Ajouterdevoir
import zipfile as z
import os
import sweetify
from .models import Enseignants,Devoirs,Categorie
from django.contrib.auth.decorators import login_required
# Create your views here.
def swwet(request):
    return render(request,'test_form.html')
def index(request):
 return render(request,'home.html')
def dashboard(request):
    user = request.user
    c=Categorie.objects.all()  
    return render(request,'dashboard.html',{'c':c})
@login_required()
def AjouterDevoir(request):
    user = request.user
    if user.is_authenticated:
        c=Categorie.objects.all() 
        if request.method == 'POST':
            titre=request.POST['titre']
            fichier=request.FILES['fichier']
            print(fichier.name)
            type_dev=request.POST['type_dev']
            #date_dep=request.POST['date_dep']
            date_fin=request.POST['date_fin']
            module=request.POST['module']
            C=Categorie.objects.get(nom=module)
            e=Enseignants.objects.get(user=user)
            #print(z.is_zipfile(fichier))
            if os.path.splitext(fichier.name)[1] != ".xlsx" and z.is_zipfile(fichier) and os.path.splitext(fichier.name)[1] != ".docx" :
                devoir=Devoirs(titre=titre,fichier=fichier,type_dev=type_dev,date_fin=date_fin,module=C,id_ens=e)
                devoir.save()
                return render(request,'dashboard.html',{'c':c})
            else:
                sweetify.sweetalert(request,'Erreur', button='Fermer',text="Le fichier que vous avez téléchargé ne correspond pas au format .zip",timer=10000,icon='warning',footer='format de  fichier à uploader est .zip')
                return redirect('dashboard')
        return render(request,'dashboard.html',{'c':c})

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

