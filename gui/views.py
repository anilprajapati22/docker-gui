from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpResponse
import docker
import time
from .models import iptableRules,wafdetails


client = docker.from_env() #start connection with docker

# Create your views here.
#shree ganeshay namah
#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

def sgn(request):
    return HttpResponse("sgnons jkh jbm jam jkh jcs jkb jjb jjb jsb jsd jam jom jsm jlm jsm jsm jkb jhd jgb jjb jd jd jd jmp jg")

def index(request):
    context={}
    return render(request, 'index.html', context)    

def getPublicIP():
    # write here code for getting public ip
    public_ip = "sgnons"
    return public_ip

def addWafDetails(container_id):
    cobjs =  [ container.attrs for container in [client.containers.get(container_id)] ]
    cobjs = [ [ d['Config']['Hostname'], d['Name'][1:], d['Id'], d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'], d['NetworkSettings']['IPAddress'] , "localhost"+":"+ d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'] , list(d['NetworkSettings']['Ports'].keys())[0] ] for d in cobjs if "container" in d['Name']] 

    waf_obj = wafdetails(
        container_id =  cobjs[0][2],
        container_name = cobjs[0][1],
        container_port = cobjs[0][3],
        container_ip = cobjs[0][4],
        public_ip = getPublicIP()
    )
    waf_obj.save()

    print("\n\n")
    print(cobjs,"\n\n")


def dockerRun(request):
    request.session['msg']=""
    if request.method == "GET":
        return render(request=request, template_name="dockerRun.html",context={
            'images' : getImages()
        })	

    if request.method == "POST":
        print(request.POST)

        is_detach=False
        #print(request.POST["is_detach"])
        #print(type(request.POST["is_detach"]))

        #if user choose multiple replica
        if request.POST.get("replica")  :       
            if int(request.POST.get("replica"))>1:
                print("\n\n\n\n\\n\n\nsgnons")
                # create port mapping 
                portMapping=docker.types.EndpointSpec(ports={int(request.POST["Hport"]):int(request.POST["Cport"])})
                created_service= client.services.create(
                        image=request.POST["image"],
                        name=request.POST["name"],
                        endpoint_spec = portMapping,
                        )

                try:
                    created_service.scale(int(request.POST['replica']))
                except:
                    print("error in scaling")  
                    request.session['msg'] = "Error In Scaling"   
                    return redirect(serviceList)
                request.session['msg'] = "Containers Created With Scaling"    
                return redirect(serviceList)


        try:
            print("\n\n\n\nsgn\n\n")
            sgncontainer = client.containers.run(request.POST["image"], 
                    detach=True,
                    ports={request.POST["Cport"]+'/tcp':request.POST["Hport"]},
                    tty = True,
                    cap_add = ['NET_ADMIN'],
                    volumes=['/home/anilprajapati/sem8/:/sgn-waf'],
                    name=request.POST["name"]+"container")
            print(sgncontainer.name) #name of the container
            print(sgncontainer.attrs)
            container_id = sgncontainer.id        
            context = { 'container_id' : container_id }

            addWafDetails(sgncontainer.attrs)

            return redirect(containerList)
            #return render(request=request, template_name="dockerRun.html",context=context)	            

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
    cobjs = [ [ d['Config']['Hostname'], d['Name'][1:], d['Id'], d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'], d['NetworkSettings']['IPAddress'] , "localhost"+":"+ d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'] , list(d['NetworkSettings']['Ports'].keys())[0] ] for d in cobjs if "container" in d['Name']] 
    print("\n\n")
    #print(cobjs.keys(),"\n\n")
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
    request.session['msg']=""
    cobj=client.containers.get(container_id)
    cobj.kill()
    cobj.remove()
    context = { "msg" : "Your Container Is Removed !!" }
    return redirect(containerList)

def containerList(request):
    cobjs =  [ container.attrs for container in client.containers.list() ]
    cobjs = [ [ d['Config']['Hostname'], d['Name'][1:], d['Id'], d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'], d['NetworkSettings']['IPAddress'] , "localhost"+":"+ d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'] , list(d['NetworkSettings']['Ports'].keys())[0] ] for d in cobjs if "container" in d['Name']] 
    context= {  "cobjs" : cobjs }
    print("\n\n")
    print(cobjs,"\n\n")
    
    return render(request=request, template_name="containerDetails.html",context=context)
 
def serviceList(request,msg=None):
    serviceattrs=[ service.attrs for service in client.services.list() ]
    cobjs = [[d["ID"] , d['Spec']['Name'], d['ID'] , d['Spec']['EndpointSpec']['Ports'][0]['PublishedPort'] , "-" , "" , d['Spec']['EndpointSpec']['Ports'][0]['TargetPort'] , d['Spec']['Mode']['Replicated']['Replicas'] ] for d in serviceattrs ]
    context = { 'services' : serviceattrs , "cobjs" : cobjs , "msg" : request.session['msg'] }
    return render(request=request, template_name="containerDetails.html",context=context)	            

def serviceRemove(request, service_id):
    # remove container
    cobj=client.services.get(service_id)
    cobj.remove()
    context = { "msg" : "Your Container Is Removed !!" }
    return redirect(serviceList)

def serviceScale(request):
    # remove container
    service_id = request.POST['service_id']

    cobj=client.services.get(service_id)
    print("\n\n\n",cobj.id)
    try:
        scale_count = int(request.POST['scale'])
        cobj.scale(scale_count)
        request.session['msg'] = "Scaling Completed"
        return redirect(serviceList)
    except:
        print("error in scaling 2")  
        request.session['msg'] = "Error In Scaling 2"   
        return redirect(serviceList)

def pullimages(request):
    if request.method == "GET":
        request.session['msg']=""
        return render(request=request, template_name="pullimages.html",context={ })	

    if request.method == "POST":
        try:
            if request.POST['tag']:        
                client.images.pull(request.POST["image"],tag=request.POST['tag'])
            else:
                client.images.pull(request.POST["image"],tag="latest")        
            return redirect(dockerRun)
        except:
            request.session['msg']="error while pulling images"
            return render(request=request, template_name="pullimages.html",context={
                'msg': request.session['msg']
             })	
