from django.http import HttpResponseRedirect
from django.shortcuts import render
from .form import DevoirForm
import os
import time

def index(request):
    if request.method == 'POST':
        form = DevoirForm(request.POST,request.FILES)
        if form.is_valid():
            nom=request.FILES['file_dev'].name
            path=os.path.abspath(".")+"\media\\files\\"
            form.save()
            os.system("javac "+path+nom)
            os.system("java "+path+nom+">>"+path+"sortie.txt")
            return HttpResponseRedirect('/students/')
    else:
        form = DevoirForm()
    return render(request,'index.html', {'form': form})

