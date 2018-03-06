import json

from django.shortcuts import render,redirect

import expertsystem.inference as IE
from account.models import Volunteer,Hospital,Pronearea,Accomadation
from controlunit.expertsystem.computation import distance
from home.models import User
from models import Food,Water,Machine,TransportGoods,TransportHuman,Rescuetool,Firstaid,Messagebox

selectedaid = []
lmap = []

from home.tests import index

def cplandinpage(request):
    if 'cusername' not in request.session:
        return redirect(index)
    return render(request,'landinpage.html',{'username':request.session['cusername']})


def controlpanel (request):
    result=[]
    if 'run' in request.POST:
        result=IE.system_run({'hazard': str(request.POST['selecthazard']),
                        'control': request.session['cusername'],
                       'span':int(request.POST['span']),
                       'lat':float(request.POST['latitude']),
                       'long':float(request.POST['longitude'])})
        return render(request, 'panel.html', {'username': request.session['cusername'],
                                              'facts':result['fact'],
                                              'field':json.dumps(result['field']),
                                              'map_data' : json.dumps(result['map_data']),
                                              'table_data':result['map_data']})
    if 'refresh' in request.POST:
        result=IE.system_run({'refresh' : "Refresh",
                              'control' : request.session['cusername']})
        return render(request, 'panel.html', {'username' : request.session['cusername'],
                                              'facts' : result['fact'],
                                              'field' : json.dumps(result['field']),
                                              'map_data': json.dumps(result['map_data']),
                                              'table_data': result['map_data']
                                              })
    if 'send' in request.POST:
        result=IE.system_run({'send':"Send",
                              'control': request.session['cusername'],
                              'selectaid':request.POST['selectaid'],
                              'parameter':request.POST['parameter']})

        return render(request, 'panel.html', {'username': request.session['cusername'],
                                              'facts': result['fact'],
                                              'field': json.dumps(result['field']),
                                              'map_data': json.dumps(result['map_data']),
                                              'table_data': result['map_data']
                                              })

    if 'deallocate' in request.POST:
        result=IE.system_run({'deallocate':"Deallocate",
                              'control': request.session['cusername']})

        return render(request, 'panel.html', {'username': request.session['cusername'],
                                              'facts': result['fact'],
                                              'field': json.dumps(result['field']),
                                              'map_data': json.dumps(result['map_data']),
                                              'table_data': result['map_data']
                                              })


    return render(request, 'panel.html',    {'username' : request.session['cusername'],
                                            })
def logout(request):
    try:
        del request.session['cusername']
    except:
        pass
    return redirect(index)


def cpmessages(request):
    try:
        if 'ack' in request.POST:
            inboxobj=Messagebox.objects.get(id=request.POST['ack'])
            inboxobj.ack=1
            inboxobj.save()
        if 'nack' in request.POST:
            inboxobj=Messagebox.objects.get(id=request.POST['nack'])
            inboxobj.nack=1
            inboxobj.save()
        inbox=Messagebox.objects.filter(toaddr=request.session['cusername'],nack=0,ack=0)
        return render(request, 'messages.html', {'username': request.session['cusername'],
                                              'inbox':inbox
                                            })
    except Messagebox.DoesNotExist:
        return render(request, 'messages.html', {'username': request.session['cusername']})


def servicelocater(request):
    altmess=""
    if 'send' in request.POST:
        m = Messagebox()
        m.fromaddr = request.session['cusername']
        m.toaddr = request.POST['send']
        m.topic = request.POST['topic']
        m.message = request.POST['message']
        m.parameter = request.POST['parameter']
        m.save()
        altmess="Message Sent Successfully"
    if 'allocate' in request.POST:
        member=User.objects.get(username=request.POST['allocate'])
        if member.category=="volunteer":
            mem=Volunteer.objects.get(user=member)
        if member.category=='hospital':
            mem=Hospital.objects.get(user=member)
        if member.category=='accommodation':
            mem=Accomadation.objects.get(user=member)
        if member.category=='pronearea':
            mem=Pronearea.objects.get(user=member)
        if mem.status==0:
            mem.status = 1
            mem.loyalto = request.session['cusername']
            mem.save()
            altmess = "User Allocated Successfully"
        else:
            altmess = "User Already Allocated"
    if 'deallocate' in request.POST:

        member=User.objects.get(username=request.POST['deallocate'])
        if member.category=="volunteer":
            mem=Volunteer.objects.get(user=member)
        if member.category=='hospital':
            mem=Hospital.objects.get(user=member)
        if member.category=='accommodation':
            mem=Accomadation.objects.get(user=member)
        if member.category=='pronearea':
            mem=Pronearea.objects.get(user=member)
        if mem.status==1:
            mem.status=0
            mem.loyalto ="nil"
            mem.save()
            altmess = "User Deallocated Successfully"
        else:
            altmess = "User Not Allocated to Deallocate"
    if 'submitlocater' in request.POST:
        selectedaid[:]=[]
        lmap[:]=[]
        if request.POST['selectaid']=='food':
            try:
                food = Food.objects.all()
                for aid in food:
                    if distance((float(request.POST['latitude']),float(request.POST['longitude'])) , (aid.user.latitude,aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title']=aid.user.username
                        tmap['lat']=aid.user.latitude
                        tmap['lng']=aid.user.longitude
                        tmap['description']="Number of current Available Packets :"+ str(aid.packet)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'volunteer':
            try:
                vol = Volunteer.objects.all()
                for aid in vol:
                    if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title'] = aid.user.username
                        tmap['lat'] = aid.user.latitude
                        tmap['lng'] = aid.user.longitude
                        tmap['description'] ="Number of current Available Volunteers :"+ str(aid.humanaid)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'hospital':
            try:
                hos = Hospital.objects.all()
                for aid in hos:
                    if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title'] = aid.user.username
                        tmap['lat'] = aid.user.latitude
                        tmap['lng'] = aid.user.longitude
                        tmap['description'] = "Number of current Available Space :"+ str(aid.canoccupy)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'accomodation':
            try:
                hos = Hospital.objects.all()
                for aid in hos:
                    if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title'] = aid.user.username
                        tmap['lat'] = aid.user.latitude
                        tmap['lng'] = aid.user.longitude
                        tmap['description'] = "Number of current Available Space to Accomodate :"+ str(aid.capacity)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'water':
            try:
                water = Water.objects.all()
                for aid in water:
                    if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title'] = aid.user.username
                        tmap['lat'] = aid.user.latitude
                        tmap['lng'] = aid.user.longitude
                        tmap['description'] = "Number of current Available Packets :"+ str(aid.quantity)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'firstaid':
            try:
                fa = Firstaid.objects.all()
                for aid in fa:
                    if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title'] = aid.user.username
                        tmap['lat'] = aid.user.latitude
                        tmap['lng'] = aid.user.longitude
                        tmap['description'] = "Number of current Available FirstAid Kit :"+ str(aid.kit)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'pronearea':
            try:
                parea = Pronearea.objects.all()
                for aid in parea:
                    if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title'] = aid.user.username
                        tmap['lat'] = aid.user.latitude
                        tmap['lng'] = aid.user.longitude
                        tmap['description'] = "Current Population :"+ str(aid.population)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'transportg':
            try:
                tg = TransportGoods.objects.all()
                for aid in tg:
                    if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title'] = aid.user.username
                        tmap['lat'] = aid.user.latitude
                        tmap['lng'] = aid.user.longitude
                        tmap['description'] = "Number of current Transportation Available :"+ str(aid.capacity)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'transporth':
            try:
                th = TransportHuman.objects.all()
                for aid in th:
                    if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title'] = aid.user.username
                        tmap['lat'] = aid.user.latitude
                        tmap['lng'] = aid.user.longitude
                        tmap['description'] = "Number of current Transportation Available :"+ str(aid.capacity)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'rescuetool':
            try:
                rt = Rescuetool.objects.all()
                for aid in rt:
                    if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                        selectedaid.append(aid)
                        tmap = {}
                        tmap['title'] = aid.user.username
                        tmap['lat'] = aid.user.latitude
                        tmap['lng'] = aid.user.longitude
                        tmap['description'] = "Number of current Rescue Tools Available :"+ str(aid.box)
                        lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'fireengine':
            try:
                m = Machine.objects.all()
                for aid in m:
                    if aid.fireengine != 0:
                        if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                    (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                            selectedaid.append(aid)
                            tmap = {}
                            tmap['title'] = aid.user.username
                            tmap['lat'] = aid.user.latitude
                            tmap['lng'] = aid.user.longitude
                            tmap['description'] = "Number of currently Fire Engines Available :"+ str(aid.fireengine)
                            lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'jcb':
            try:
                m = Machine.objects.all()
                for aid in m:
                    if aid.jcb != 0:
                        if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                    (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                            selectedaid.append(aid)
                            tmap = {}
                            tmap['title'] = aid.user.username
                            tmap['lat'] = aid.user.latitude
                            tmap['lng'] = aid.user.longitude
                            tmap['description'] = "Number of currently JCB Available :"+ str(aid.jcb)
                            lmap.append(tmap)
            except Food.DoesNotExist:
                pass
        if request.POST['selectaid'] == 'ambulance':
            try:
                m = Machine.objects.all()
                for aid in m:
                    if aid.ambulance != 0:
                        if distance((float(request.POST['latitude']), float(request.POST['longitude'])),
                                    (aid.user.latitude, aid.user.longitude)) <= float(request.POST['distance']):
                            selectedaid.append(aid)
                            tmap = {}
                            tmap['title'] = aid.user.username
                            tmap['lat'] = aid.user.latitude
                            tmap['lng'] = aid.user.longitude
                            tmap['description'] = "Number of current Ambulance Available :"+ str(aid.ambulance)
                            lmap.append(tmap)
            except Food.DoesNotExist:
                pass
    return render(request, 'locater.html',{'username': request.session['cusername'],
                                           'selectedaid': selectedaid,'mapelt':json.dumps(lmap),
                                           'altmess':json.dumps(altmess),
                                           })

def responsebox(request):
    try:
        inbox=Messagebox.objects.filter(fromaddr=request.session['cusername'])
        return render(request, 'Allmessages.html', {'username': request.session['cusername'],
                                              'inbox':inbox
                                            })
    except Messagebox.DoesNotExist:
        return render(request, 'Allmessages.html', {'username': request.session['cusername']})