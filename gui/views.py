from multiprocessing import context
from django.shortcuts import render,redirect
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
        return render(request=request, template_name="dockerRun.html",context={
            'images' : getImages()
        })	

    if request.method == "POST":
        print(request.POST)
        is_detach=False
        #print(request.POST["is_detach"])
        #print(type(request.POST["is_detach"]))
        if request.POST.get("is_detach"):
            is_detach=True
            print(is_detach) 
        try:
            sgncontainer = client.containers.run(request.POST["image"], 
                    detach=is_detach,
                    ports={request.POST["Cport"]+'/tcp':request.POST["Hport"]},
                    #volumes=['/home/anil/sem8:/sgn-waf'],
                    name=request.POST["name"])
            print(sgncontainer.name) #name of the container
            print(sgncontainer.attrs)
            container_id = sgncontainer.id        
            context = { 'container_id' : container_id }
            return render(request=request, template_name="dockerRun.html",context=context)	            

        except:
            print("sgnons error")

            #if same name container was there
            if "sgn-python" in [container.name for container in client.containers.list()]:
                print("container name is already there ! please change the name")
            return render(request=request, template_name="dockerRun.html",context={})	
	


#{% url '{{ containerLink }}' %}

def containerDetails(request, container_id ):
    #get containers details from attr
    cobj=client.containers.get(container_id)
    cobjs = [ cobj.attrs ]
    #cobjs =  [ container.attrs for container in client.containers.list() ]
    cobjs = [ [ d['Config']['Hostname'], d['Name'][1:], d['Id'], d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'], d['NetworkSettings']['IPAddress'] , "localhost"+":"+ d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'] , list(d['NetworkSettings']['Ports'].keys())[0] ] for d in cobjs ] 

    context= {  "cobjs" : cobjs, "cid" : cobj.attrs['Id'][:10] , "container_id"  :  container_id }
    return render(request=request, template_name="containerDetails.html",context=context)

def containerRemove(request, container_id):
    # remove container
    cobj=client.containers.get(container_id)
    cobj.kill()
    cobj.remove()
    context = { "msg" : "Your Container Is Removed !!" }
    return render(request=request, template_name="containerDetails.html",context=context)
            
def getImages():
    images=[image.tags[0] for image in  client.images.list() if image.tags]
    return images

def containerRemove(request, container_id):
    # remove container
    cobj=client.containers.get(container_id)
    cobj.kill()
    cobj.remove()
    context = { "msg" : "Your Container Is Removed !!" }
    return redirect(containerList)

def containerList(request):
    cobjs =  [ container.attrs for container in client.containers.list() ]
    cobjs = [ [ d['Config']['Hostname'], d['Name'][1:], d['Id'], d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'], d['NetworkSettings']['IPAddress'] , "localhost"+":"+ d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'] , list(d['NetworkSettings']['Ports'].keys())[0] ] for d in cobjs ] 
    context= {  "cobjs" : cobjs }
    return render(request=request, template_name="containerDetails.html",context=context)
 

