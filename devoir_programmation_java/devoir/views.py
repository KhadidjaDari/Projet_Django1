from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import template
from django.template import loader
from .forms import Ajouterdevoir
import zipfile as z
import re
import os
import sweetify
from .models import Enseignants,Devoirs,Categorie,Etudiant
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
def VerfierCondition(f):
    try:
        lire=z.ZipFile(f,mode='r',)
        list_name=lire.namelist()
        print(list_name)
        e=r'\w\.pdf'
        w=None
        for h in list_name:
            if re.search(e,h):
                w=re.search(e,h)
        l=['in.txt','out.txt']
        a=False
        for q in l:
            a=any(q in s for s in list_name)
        if a and w:
            return True
        else :
            return False
        
    except ValueError:
        print(ValueError)





@login_required()
def AjouterDevoir(request):
    user = request.user
    if user.is_authenticated:
        c=Categorie.objects.all() 
        if request.method == 'POST':
            titre=request.POST['titre']
            fichier=None
            try:
                fichier=request.FILES['fichier']
            except:
                sweetify.sweetalert(request,'Erreur', button='ok',text="le fichier vide",timer=10000,icon='warning')
                return redirect('dashboard')
            type_dev=request.POST['type_dev']
            date_fin=request.POST['date_fin']
            module=request.POST['module']
            if len(titre) == 0 or fichier == None or len(type_dev) == 0 or len(date_fin) == 0 or len(module) == 0:
                sweetify.sweetalert(request,'Erreur', button='ok',text="Il y a un champ que vous n'avez pas rempli",timer=10000,icon='warning')
                return redirect('dashboard')
            C=Categorie.objects.get(nom=module)
            e=Enseignants.objects.get(user=user)
            i=str(user.pk)
            try:
                d=Devoirs.objects.get(titre=titre,fichier='devoir/'+titre+'_'+i+'.zip',type_dev=type_dev,date_fin=date_fin,module=C,id_ens=e)
                if d!= None:
                    sweetify.sweetalert(request,'Erreur', button='ok',text="le devoir déjà existé",timer=10000,icon='warning')
                    return redirect('dashboard')
            except:
                print("")
            if os.path.splitext(fichier.name)[1] != ".xlsx" and z.is_zipfile(fichier) and os.path.splitext(fichier.name)[1] != ".docx" :
                if VerfierCondition(fichier):
                    devoir=Devoirs(titre=titre,fichier=fichier,type_dev=type_dev,date_fin=date_fin,module=C,id_ens=e)
                    devoir.save()
                    old_file = os.path.join("C:\\Users\\Khadija\\Desktop\\Django_Projects\\devoir_programmation_java\\media\\devoir",fichier.name)
                    new_file = os.path.join("C:\\Users\\Khadija\\Desktop\\Django_Projects\\devoir_programmation_java\\media\\devoir",titre+'_'+i+'.zip')
                    os.rename(old_file, new_file)
                    devoir.fichier='devoir/'+titre+'_'+i+'.zip'
                    devoir.save()
                    sweetify.sweetalert(request,'Ajouter Devoir', button='ok',text="Ajouté avec succès",timer=10000,icon='success',)
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
        if load_template == 'settings.html':
            return redirect('Profil')
            
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist :

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))


@login_required()
def Profil(request):
    user = request.user
    e=None
    if user.type_cmp == 'Enseignant':
        e=Enseignants.objects.get(user=user)
    if user.type_cmp == 'Etudiant':
        e=Etudiant.objects.get(user=user)
    return render(request,'settings.html',{'e':e})