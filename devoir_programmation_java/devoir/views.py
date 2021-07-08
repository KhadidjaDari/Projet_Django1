from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import template
from django.template import loader
from .forms import Ajouterdevoir
import zipfile as z
import re
import os
import sweetify
from .models import Enseignants,Devoirs,Categorie,Etudiant,Soumission
from django.contrib.auth.decorators import login_required
from pathlib import Path
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
import time
# Create your views here.
@login_required()
def MesDevoir(request):
    user = request.user
    e=None
    if user.type_cmp == 'Enseignant':
        e=Enseignants.objects.get(user=user)
        devoirs=Devoirs.objects.filter(id_ens=e.pk).values()
    return render(request,'mes_devoir.html',{'e':e,'devoirs':devoirs})
@login_required()
def listEtudiant(request):
    user = request.user
    e=None
    etuds=Etudiant.objects.all()
    if user.type_cmp == 'Enseignant':
        e=Enseignants.objects.get(user=user)
    return render(request,'list_etudiants.html',{'e':e,'etuds':etuds})
def Verifier_Fichier_Solution(fichier):
    try:
        lire=z.ZipFile(fichier,mode='r')
        list_name=lire.namelist()
        e='main.java'
        w=None
        for h in list_name:
            if re.search(e,h):
                w=h
        return w
    except ValueError:
        print(ValueError)
        return w
@login_required()
def Soumission_Etud(request,id_dev):
    user = request.user
    if request.method == 'POST':
        fichier=None
        try:
            fichier=request.FILES['solution']
            if os.path.splitext(fichier.name)[1] != ".xlsx" and z.is_zipfile(fichier) and os.path.splitext(fichier.name)[1] != ".docx" :
                if Verifier_Fichier_Solution(fichier) !=None:
                    w=Verifier_Fichier_Solution(fichier)
                    lire=z.ZipFile(fichier,mode='r')
                    with lire.open(w) as myfile:
                        source=myfile.read()
                        main=open("C:/Users/Khadija/Desktop/Django_Projects/devoir_programmation_java/media/solutions/main.java",'wb')
                        main.write(source)
                        main.close()
                        #os.chdir == cd 
                        os.chdir("C:/Users/Khadija/Desktop/Django_Projects/devoir_programmation_java/media/solutions")
                        os.system("javac main.java 2> erreur.txt")
                        size=os.path.getsize("erreur.txt")
                        if size > 0:
                            erreur=open("erreur.txt").read().split('\n|,|;|^')
                            sweetify.sweetalert(request,'Erreur', button='ok',text=erreur,timer=200000,icon='error')
                            return redirect('dashboard')
                        if size == 0:
                            try:
                                devoir=Devoirs.objects.get(id=id_dev)
                                nom_fichier=devoir.fichier
                                zip_devoir=z.ZipFile(nom_fichier,mode='r',)
                                list_name=zip_devoir.namelist()
                                in_txt="in.txt"
                                out_txt="out.txt"
                                for h in list_name:
                                    if re.search(in_txt,h):
                                        in_txt=h
                                    if  re.search(out_txt,h):
                                        out_txt=h
                                entre=open("in.txt","wb")
                                with zip_devoir.open(in_txt) as i:
                                    entre.write(i.read())
                                    entre.close()
                                out_put=open("out.txt","wb")
                                with zip_devoir.open(out_txt) as o:
                                    out_put.write(o.read())
                                    out_put.close
                                os.system("java main.java<in.txt >>sortie.txt")
                                
                            except:
                                sweetify.sweetalert(request,'Erreur', button='ok',text="Il y a une erreur ou le devoir a été supprimé",timer=200000,icon='error')
                                return redirect('dashboard')

                        #time.sleep(10)
                        #os.system("java C:/Users/Khadija/Desktop/Django_Projects/devoir_programmation_java/media/solutions/main.java >> C:/Users/Khadija/Desktop/Django_Projects/devoir_programmation_java/media/solutions/sortie.txt")
                        return redirect('dashboard')
                else:
                    sweetify.sweetalert(request,'Erreur', button='ok',text="le fichier ne contient pas main.java",timer=10000,icon='warning')
                    return redirect('dashboard')
            else:
                sweetify.sweetalert(request,'Erreur', button='Fermer',text="Le fichier que vous avez téléchargé ne correspond pas au format .zip",timer=10000,icon='warning',footer='format de  fichier à uploader est .zip')
                return redirect('dashboard')

        except ValueError:
            print(ValueError)
            sweetify.sweetalert(request,'Erreur', button='ok',text="le fichier vide",timer=10000,icon='warning')
            return redirect('dashboard')


def swwet(request):
    return render(request,'test_form.html')



def index(request):
 return render(request,'home.html')




@login_required()
def dashboard(request):
    user = request.user
    c=Categorie.objects.all() 
    e=None
    if user.type_cmp == 'Etudiant':
        e=Etudiant.objects.get(user=user)
        list_devoirs=[]
        soum=None
        if e.promo != None:
            try:
                soum=Soumission.objects.filter(id_etud=e.pk).values()
                s=[format(q['id_dev_id']) for q in soum]
                s = list(map(int,s))
            except:
                soum=None
                s=None
            try:
                c=Categorie.objects.filter(promo=e.promo)
                for cat in c:
                    list_devoirs.append(Devoirs.objects.filter(module=cat).values())
                khadidja=[]
                for k in list_devoirs:
                    p=[format(d['id']) for d in k]
                    khadidja.append(p)
                devoirs=[]
                for i in khadidja:
                    for g in i:
                        devoirs.append(Devoirs.objects.get(id=g))
                return render(request,'dashboard.html',{'devoirs':devoirs,'e':e,'s':s})
            except:
                sweetify.sweetalert(request,'List des devoirs', button='ok',text="Il n'y a pas de devoirs pour votre promotion !!!",timer=10000,icon='info',)
                return render(request,'dashboard.html',{'e':e})
    if user.type_cmp == 'Enseignant':
        e=Enseignants.objects.get(user=user) 
    return render(request,'dashboard.html',{'c':c,'e':e})











def VerfierCondition(f):
    try:
        lire=z.ZipFile(f,mode='r',)
        list_name=lire.namelist()

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
            return redirect('dashboard')
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
def ModifierInfo(request):
    user = request.user
    if request.method == 'POST':
        nom=None
        if request.POST['nom']:
            nom=request.POST['nom']
        prenom=None
        if request.POST['prenom']:
            prenom=request.POST['prenom']
        date_naiss=None
        if request.POST['date_naiss']:
            date_naiss=request.POST['date_naiss']
        e=None
        if user.type_cmp == 'Etudiant':
            promo=None
            if request.POST['promo']:
                promo=request.POST['promo']
            if nom == None and prenom == None and date_naiss == None and promo == None:
                sweetify.sweetalert(request,'Erreur', button='ok',text="Information non renseignée ",timer=10000,icon='warning')
 
            e=Etudiant.objects.get(user=user)
            if nom != None:
                e.nom=nom
            if prenom != None:
                e.prenom=prenom
            if date_naiss != None:
                e.date_naiss=date_naiss
            if promo != None:
                e.promo=promo
            e.save()
            sweetify.sweetalert(request,'Modification les informations personnelle', button='ok',text="Modifie avec succès",timer=10000,icon='success',)
            return redirect('Profil')
        if user.type_cmp == 'Enseignant':
            grade=None
            if request.POST['grade']:
                grade=request.POST['grade']
            if nom == None and prenom == None and date_naiss == None and grade == None:
                sweetify.sweetalert(request,'Erreur', button='ok',text="Information non renseignée ",timer=10000,icon='warning')
            e=Enseignants.objects.get(user=user)
            if nom != None:
                e.nom=nom
            if prenom != None:
                e.prenom=prenom
            if date_naiss != None:
                e.date_naiss=date_nais
            if grade != None:
                e.grade=grade
            e.save()
            sweetify.sweetalert(request,'Modification les informations personnelle', button='ok',text="Modifie avec succès",timer=10000,icon='success',)
            return redirect('Profil')
    else:
        return redirect('Profil')



@login_required()  
def ModifierAvatar(request):   
    user = request.user
    if request.method == 'POST':
        img=request.FILES['avatar']
        if user.type_cmp == 'Etudiant':
           e=Etudiant.objects.get(user=user)
           e.avatar=img
           e.save()
           sweetify.sweetalert(request,'Modification image', button='ok',text="Modifie avec succès",timer=10000,icon='success',)

           return redirect('Profil')
        if user.type_cmp == 'Enseignant':
            e=Enseignants.objects.get(user=user)
            e.avatar=img
            e.save()
            sweetify.sweetalert(request,'Modification image', button='ok',text="Modifie avec succès",timer=10000,icon='success',)
            return redirect('Profil')
    else:
        return redirect('Profil')
@login_required()
def Profil(request):
    user = request.user
    e=None
    if user.type_cmp == 'Enseignant':
        e=Enseignants.objects.get(user=user)
    if user.type_cmp == 'Etudiant':
        e=Etudiant.objects.get(user=user)
    return render(request,'settings.html',{'e':e})




@login_required()
def ListDevoir(request):
    user = request.user
    if user.type_cmp == 'Etudiant':
        e=Etudiant.objects.get(user=user)
        list_devoirs=[]
        c=None
        if e.promo != None:
            try:
                c=Categorie.objects.filter(promo=e.promo)
            except:
                sweetify.sweetalert(request,'List des devoirs', button='ok',text="cette promotion ",timer=10000,icon='error',)

            for cat in c:
                list_devoirs.append(Devoirs.objects.filter(module=cat).values())
            p=[format(d['id']) for d in list_devoirs[0]]
            devoirs=[]
            for i in p:
                devoirs.append(Devoirs.objects.get(id=i))
            return render(request,'tt.html',{'devoirs':devoirs})
        else :
            return render(request,'tt.html')
    else:
        return render(request,'tt.html')


@login_required()
def AfficheDevoir(request,id_dev):
    try:
        devoir=Devoirs.objects.get(id=id_dev)
        nom_fichier=devoir.fichier
        lire=z.ZipFile(nom_fichier,mode='r',)
        list_name=lire.namelist()
        print(list_name)
        e=r'\w\.pdf'
        w=None
        for h in list_name:
            if re.search(e,h):
                w=h
        print(w)
        with lire.open(w) as myfile:
            output_filename ='C:/Users/Khadija/Desktop/Django_Projects/devoir_programmation_java/media/devoir/devoir.pdf'
            document=PdfFileReader(myfile)
            writer = PdfFileWriter()
            for x in range(document.numPages):
                page=document.getPage(x)
                writer.addPage(page)
            with open(output_filename, 'wb') as fp:
                writer.write(fp)
            #os.system(output_filename)
            """pdftext = ""
            for page in range(document.numPages):
                pageObj = document.getPage(page)
                pdftext += pageObj.extractText().replace('\n','')
            print(pdftext)
            return render(request,'affiche_devoir.html',{'devoir':devoir})"""
            return redirect('/media/devoir/devoir.pdf')
    except ValueError:
        print(ValueError)
        return render(request,'page-404.html')