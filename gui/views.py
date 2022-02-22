from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
import docker
client = docker.from_env() #start connection with docker

# Create your views here.
#shree ganeshay namah
#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

def sgn(request):
    return HttpResponse("sgnons jkh jbm jam jkh jcs jkb jjb jjb jsb jsd jam jom jsm jlm jsm jsm jkb jhd jgb jjb jd jd jd jmp jg")

def index(request):
    context={}
    return render(request, 'index.html', context)    

def dockerRun(request):
    if request.method == "GET":
        return render(request=request, template_name="dockerRun.html",context={})	

    if request.method == "POST":
        print(request.POST)
        return render(request=request, template_name="dockerRun.html",context={})	


