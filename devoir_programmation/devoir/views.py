from django.shortcuts import render
from django.http import HttpResponse
from django import template
from django.template import loader
# Create your views here.
def index(request):
 return render(request,'home.html')
"""def dashboard(request):
 return render(request,'dashboard.html')"""
def reg(request):
 return render(request,'register.html')
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
