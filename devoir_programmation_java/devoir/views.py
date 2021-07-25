from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import template
from django.contrib import messages
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
import filecmp 
import warnings
import time
from django.db.models.signals import post_save
from notifications.signals import notify
# Create your views here.
path=os.path.abspath(".")+"\media"
chemin=os.path.abspath(".")
def TestTrue(fichier1,fichier2,path):
    f1=None
    f2=None
    if path == "":
        f1=fichier1
        f2=fichier2
    else:
        f1=path+fichier1
        f2=path+fichier2
    if os.path.getsize(f1)==os.path.getsize(f2):
        if filecmp.cmp(f1,f2):
            return True
    f_max=None
    f_min=None
    if os.path.getsize(f1)>os.path.getsize(f2):
        f_max=f1
        f_min=f2
    if os.path.getsize(f2)>os.path.getsize(f1):
        f_max=f2
        f_min=f1
    a=open(f_max).read().split('\n')
    b=open(f_min).read().split('\n')
    if len(a)==len(b)+1:
        if a[-1]== "":
            if b  == a[0:-1]:
                return True
            else :
                return False
    return False

def Verifier_Fichier_Solution(fichier):
    try:
        lire=z.ZipFile(fichier,mode='r')
        list_name=lire.namelist()
        e='main.java'
        w=False
        for h in list_name:
            if re.search(e,h):
                w=True
        return w
    except ValueError:
        print(ValueError)
        return w
        
@login_required()
def MesDevoir(request):
    user = request.user
    c=Categorie.objects.all()
    e=None
    if user.type_cmp == 'Enseignant':
        e=Enseignants.objects.get(user=user)
        devoirs=Devoirs.objects.filter(id_ens=e.pk)
        etudiant=Etudiant.objects.get(id=1)
        #notify.send(etudiant,recipient=user,verb="test notification")
    return render(request,'mes_devoir.html',{'e':e,'devoirs':devoirs,'c':c})
@login_required()
def listEtudiant(request):
    user = request.user
    e=None
    etuds=Etudiant.objects.all()
    if user.type_cmp == 'Enseignant':
        e=Enseignants.objects.get(user=user)
    return render(request,'list_etudiants.html',{'e':e,'etuds':etuds})

@login_required()
def Soumission_Etud(request,id_dev,id_etud):
    user=request.user
    if request.method == 'POST' and user.type_cmp=="Etudiant":
        Note=0
        fichier=None
        try:
            fichier=request.FILES['solution']
        except:
            sweetify.sweetalert(request,'Erreur', button='ok',text="Vous n'avez pas uploade le fichier !!",timer=10000,icon='warning')
            return redirect('dashboard')
        if os.path.splitext(fichier.name)[1] != ".xlsx" and z.is_zipfile(fichier) and os.path.splitext(fichier.name)[1] != ".docx" :
            #########   mna ############
            if Verifier_Fichier_Solution(fichier):
                with z.ZipFile(fichier) as lire:
                    for qr in lire.namelist():
                        with lire.open(qr) as myfile:
                            #os.chdir == cd 
                            os.chdir(path+"\solutions")
                            try:
                                fr=str(qr).split('/')[1]
                            except:
                                fr=str(qr)
                            if fr !="":
                                prog=open(fr,"wb")
                                prog.write(myfile.read())
                                prog.close()
                    os.system("javac main.java 2> erreur.txt")
                    size=os.path.getsize("erreur.txt")
                    #########   mna ############
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
                                if re.search(out_txt,h):
                                    out_txt=h
                            entre=open("in.txt","wb")
                            with zip_devoir.open(in_txt) as i:
                                entre.write(i.read())
                                entre.close()
                                out_put=open("out.txt","wb")
                            with zip_devoir.open(out_txt) as o:
                                out_put.write(o.read())
                                out_put.close()
                                if os.path.exists("sortie.txt"):
                                    os.remove("sortie.txt")#pour supprimer sortie.txt
                                q=False
                                start_time=time.time()
                                os.system("java main < in.txt >> sortie.txt")
                                interval=time.time()-start_time
                                print(interval)
                                q=TestTrue("sortie.txt","out.txt",path+"\solutions\\")
                                for qr in lire.namelist():
                                    try:
                                        fr=str(qr).split('/')[1]
                                    except:
                                        fr=str(qr)
                                    if os.path.exists(str(fr)):
                                        os.remove(str(fr))
                                        os.remove(str(fr).split('.')[0]+".class")
                                if q:
                                    Note=5
                                    os.chdir(chemin)
                                    etudiant=Etudiant.objects.get(id=id_etud)
                                    som_dev=None
                                    if Soumission.objects.filter(id_etud=etudiant,id_dev=devoir).values():
                                        som_dev=Soumission.objects.filter(id_etud=etudiant,id_dev=devoir).values()
                                    if som_dev == None:
                                        som=Soumission(id_etud=etudiant,id_dev=devoir,note=Note,solution=fichier)
                                        som.save()
                                        old_file = os.path.join(path+"\solutions",fichier.name)
                                        new_file = os.path.join(path+"\solutions",fichier.name.split('.')[0]+'_'+i+'.zip')
                                        os.rename(old_file, new_file)
                                        som.solution='solutions/'+fichier.name.split('.')[0]+'_'+i+'.zip'
                                        som.save()
                                        sweetify.sweetalert(request,'Evaluation',text="la note de votre soumission est "+str(Note)+"/5",timer=10000,icon='success',)
                                        return redirect('dashboard')
                                    else:
                                        dd=[format(d['id']) for d in som_dev]
                                        gg=Soumission.objects.get(id=dd[0])
                                        solution_name=str(gg.solution)
                                        if os.path.exists(path+"/"+solution_name):
                                            os.remove(path+"/"+solution_name)
                                        gg.delete()
                                        som=Soumission(id_etud=etudiant,id_dev=devoir,note=Note,solution=fichier)
                                        som.save()
                                        old_file = os.path.join(path+"\solutions",fichier.name)
                                        print(old_file)
                                        i=str(user.pk)
                                        new_file=os.path.join(path+"\solutions",fichier.name.split('.')[0]+'_'+i+'.zip')
                                        os.rename(old_file,new_file)
                                        som.solution='solutions/'+fichier.name.split('.')[0]+'_'+i+'.zip'
                                        som.save()
                                        sweetify.sweetalert(request,'Evaluation', button='ok',text="la note de votre soumission est "+str(Note)+"/5",timer=10000,icon='success',)
                                        return redirect('dashboard')
                                else:
                                    sweetify.sweetalert(request,'Evaluation', button='ok',text="la note de votre soumission est "+str(Note)+"/5 vérifier votre code",timer=10000,icon='warning',)
                                    return redirect('dashboard')
                        except:
                            sweetify.sweetalert(request,'Erreur', button='ok',text="Il y a une erreur ou le devoir a été supprimé",timer=200000,icon='error')
                            return redirect('dashboard')
            else:
                sweetify.sweetalert(request,'Erreur', button='ok',text="le fichier ne contient pas main.java",timer=10000,icon='warning')
                return redirect('dashboard')
        else:
            sweetify.sweetalert(request,'Erreur', button='Fermer',text="Le fichier que vous avez téléchargé ne correspond pas au format .zip",timer=10000,icon='warning',footer='format de  fichier à uploader est .zip')
            return redirect('dashboard')   #probleme f return redirect
    else:
        return redirect('dashboard')
            




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
                sweetify.sweetalert(request,'Erreur', button='ok',text="Vous n'avez pas uploade le fichier !!",timer=10000,icon='warning')
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
                    old_file = os.path.join(path+"\devoir",fichier.name)
                    new_file = os.path.join(path+"\devoir",titre+'_'+i+'.zip')
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
        img=None
        try:
            img=request.FILES['avatar']
        except:
            sweetify.sweetalert(request,'Erreur', button='ok',text="Vous n'avez pas uploade l'image !!",timer=10000,icon='warning')
            return redirect('Profil')
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
            output_filename =path+"\devoir\devoir.pdf"
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
@login_required()
def SupprimerDevoir(request,id_dev):
    user = request.user
    if user.type_cmp == 'Enseignant':
        try:
            e=Enseignants.objects.get(user=user)
            devoirs=Devoirs.objects.filter(id_ens=e)
            d=Devoirs.objects.get(id=id_dev)
            titre=d.titre
            fichier=d.fichier
            if d in devoirs:
                d.delete()
                os.chdir(path+"\devoir")
                f=str(fichier)
                if os.path.exists(f.split('/')[1]):
                    os.remove(path+"/"+str(fichier))
                sweetify.sweetalert(request,'Suppression de devoir', button='ok',text="Suppression avec succès de devoir "+titre,timer=30000,icon='success',)
                return redirect('MesDevoir')
            else:
                sweetify.sweetalert(request,'Erreur', button='ok',text="ce devoir n'existe pas !!! ",timer=30000,icon='warning')
                return redirect('MesDevoir')
        except:
            return render(request,'page-500.html')
    else:
        return render(request,'page-404.html')


@login_required()
def ModifierDevoir(request,id_dev):
    user=request.user
    if user.type_cmp == 'Enseignant' and request.method == 'POST':
        titre=None
        type_dev=None
        fichier=None
        date_fin=None
        module=None
        try:
            e=Enseignants.objects.get(user=user)
            devoirs=Devoirs.objects.filter(id_ens=e)
            d=Devoirs.objects.get(id=id_dev)
            fil=d.fichier
            if request.POST['titre']:
                titre=request.POST['titre']
            if request.POST['type_dev']:
                type_dev=request.POST['type_dev']
            try:
                fichier=request.FILES['fichier']
            except:
                fichier=None
            if request.POST['date_fin']:
                date_fin=request.POST['date_fin']
            if request.POST['module']:
                module=request.POST['module']
            if titre == None and type_dev == None and fichier == None and date_fin == None and module == None:
                sweetify.sweetalert(request,'Modification de devoir', button='ok',text="Tu n'as rien changé !! ",timer=30000,icon='warning',)
                return redirect('MesDevoir')  
            if d in devoirs:
                if titre != None:
                    d.titre=titre
                if type_dev !=  None:
                    d.type_dev=type_dev
                if fichier != None:
                    if os.path.splitext(fichier.name)[1] == ".xlsx" or not z.is_zipfile(fichier) or os.path.splitext(fichier.name)[1] == ".docx" :
                        sweetify.sweetalert(request,'Erreur', button='Fermer',text="Le fichier que vous avez téléchargé ne correspond pas au format .zip",timer=10000,icon='warning',footer='format de  fichier à uploader est .zip')
                        return redirect('MesDevoir')
                    os.chdir(path+"\devoir")
                    f=str(fil)
                    if os.path.exists(f.split('/')[1]):
                        os.remove(path+"/"+str(fil))
                    d.fichier=fichier
                    d.save()
                    old_file = os.path.join(path+"\devoir",fichier.name)
                    new_file = os.path.join(path+"\devoir",str(fil).split('/')[1])
                    os.rename(old_file,new_file)
                    d.fichier="devoir/"+str(fil).split('/')[1]
                if date_fin != None:
                    d.date_fin=date_fin
                if module != None:
                    C=Categorie.objects.get(nom=module)
                    d.module=C
                d.save()
                sweetify.sweetalert(request,'Modification de devoir', button='ok',text="Modification avec succès de devoir ",timer=30000,icon='success',)
                return redirect('MesDevoir')
        except:
            return render(request,'page-500.html')
        return redirect('MesDevoir')
    else:
        return render(request,'page-404.html')

@login_required()
def QuiFaitDevoir(request,id_dev):
    user=request.user
    if user.type_cmp =='Enseignant':
        try:
            e=Enseignants.objects.get(user=user)
            devoirs=Devoirs.objects.filter(id_ens=e)
            d=Devoirs.objects.get(id=id_dev)
            if d in devoirs:
                soum=Soumission.objects.filter(id_dev=d)
                return render(request,"QuiFaitDevoir.html",{'soum':soum,"e":e})         
        except:
           return render(request,'page-500.html') 
    return redirect('MesDevoir')
