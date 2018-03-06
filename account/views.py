from django.shortcuts import render ,redirect

from home.models import User

import json

from models import Volunteer,Hospital,Pronearea,Accomadation

from controlunit.models import  Food,Water,Machine,TransportGoods,TransportHuman,Rescuetool,Firstaid,Messagebox

from home.tests import index

def landinpage(request):

    if 'username' not in request.session:
        return redirect(index)
    return render(request,'homepage.html',{'username':request.session['username']})


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect(index)


def updateresources(request):
    if 'username' not in request.session:
        return redirect(index)

    new_user = User.objects.get(username=request.session['username'])
    cate =new_user.category
    try:
        f = Food.objects.get(user=new_user)
        food = f.packet
    except Food.DoesNotExist:
        food = 0
    try:
        w = Water.objects.get(user=new_user)
        water = w.quantity
    except Water.DoesNotExist:
        water = 0
    try:
        fa = Firstaid.objects.get(user=new_user)
        firstaid = fa.kit
    except Firstaid.DoesNotExist:
        firstaid = 0
    try:
        r = Rescuetool.objects.get(user=new_user)
        rescuetools = r.box
    except Rescuetool.DoesNotExist:
        rescuetools = 0

    try:
        m = Machine.objects.get(user=new_user)
        fireengine = m.fireengine
        ambulance = m.ambulance
        jcb = m.jcb
    except Machine.DoesNotExist:
        fireengine = 0
        ambulance = 0
        jcb = 0
    try:
        t = TransportHuman.objects.get(user=new_user)
        tgoods = t.capacity
    except TransportHuman.DoesNotExist:
        tgoods = 0

    try:
        t = TransportGoods.objects.get(user=new_user)
        thuman=t.capacity
    except TransportGoods.DoesNotExist:
        thuman=0

    if "submitfood" in request.POST:
        try:
            f = Food.objects.get(user=new_user)
        except Food.DoesNotExist:
            f=Food()
            f.user=new_user
        f.packet = request.POST['packet']
        f.save()
        return render(request, 'updateres.html',    {'username': request.session['username'], 'req': "success" ,
                                                    'cat' : new_user.category,
                                                    'food' : f.packet,
                                                    'water' :water,
                                                    'firstaid':firstaid,
                                                    'rescuetool' : rescuetools,
                                                    'fireengine' : fireengine,
                                                    'jcb' : jcb,
                                                    'ambulance':ambulance,
                                                    'tgoods' : tgoods,
                                                    'thuman' : thuman,
                                                    'category': json.dumps(cate)
                                                    })
    if "submitwater" in request.POST:
        try:
            w = Water.objects.get(user=new_user)
        except Water.DoesNotExist:
            w = Water()
            w.user=new_user
        w.quantity = request.POST['quantity']
        w.save()
        return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                  'cat': new_user.category,
                                                  'food': food,
                                                  'water': w.quantity ,
                                                  'firstaid': firstaid,
                                                  'rescuetool': rescuetools,
                                                  'fireengine': fireengine,
                                                  'jcb': jcb,
                                                  'ambulance': ambulance,
                                                  'tgoods': tgoods,
                                                  'thuman': thuman,
                                                  'category': json.dumps(cate)
                                                  })
    if "submitfirstaid" in request.POST:
        try:
            fa = Firstaid.objects.get(user=new_user)
        except Firstaid.DoesNotExist:
            fa = Firstaid()
            fa.user = new_user
        fa.kit = request.POST['kit']
        fa.save()
        return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                  'cat': new_user.category,
                                                  'food': food,
                                                  'water': water,
                                                  'firstaid': fa.kit,
                                                  'rescuetool': rescuetools,
                                                  'fireengine': fireengine,
                                                  'jcb': jcb,
                                                  'ambulance': ambulance,
                                                  'tgoods': tgoods,
                                                  'thuman': thuman,
                                                  'category': json.dumps(cate)
                                                  })
    if "submitrescuetool" in request.POST:
        try:
            r = Rescuetool.objects.get(user=new_user)
        except Rescuetool.DoesNotExist:
            r = Rescuetool()
            r.user = new_user
        r.box = request.POST['box']
        r.save()
        return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                  'cat': new_user.category,
                                                  'food': food,
                                                  'water': water,
                                                  'firstaid': firstaid,
                                                  'rescuetool': r.box,
                                                  'fireengine': fireengine,
                                                  'jcb': jcb,
                                                  'ambulance': ambulance,
                                                  'tgoods': tgoods,
                                                  'thuman': thuman,
                                                  'category': json.dumps(cate)
                                                  })
    if "submitmachine" in request.POST:
        try:
            m = Machine.objects.get(user=new_user)
        except Machine.DoesNotExist:
            m = Machine()
            m.user = new_user
        m.fireengine = request.POST['fireengine']
        m.jcb = request.POST['jcb']
        m.ambulance = request.POST['ambulance']
        m.save()
        return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                  'cat': new_user.category,
                                                  'food': food,
                                                  'water': water,
                                                  'firstaid': firstaid,
                                                  'rescuetool': rescuetools,
                                                  'fireengine': m.fireengine,
                                                  'jcb': m.jcb,
                                                  'ambulance': m.ambulance,
                                                  'tgoods': tgoods,
                                                  'thuman': thuman,
                                                  'category': json.dumps(cate)
                                                  })
    if "submittransport" in request.POST:
        if request.POST['typeofvehicle']=="Goods":
            try:
                t = TransportGoods.objects.get(user=new_user)
            except TransportGoods.DoesNotExist:
                t = TransportGoods()
                t.user = new_user
            t.capacity = request.POST['capacity']
            t.save()
            return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                      'cat': new_user.category,
                                                      'food': food,
                                                      'water': water,
                                                      'firstaid': firstaid,
                                                      'rescuetool': rescuetools,
                                                      'fireengine': fireengine,
                                                      'jcb': jcb,
                                                      'ambulance': ambulance,
                                                      'tgoods': t.capacity,
                                                      'thuman': thuman,
                                                      'category': json.dumps(cate)
                                                      })
        if request.POST['typeofvehicle']=="Human":
            try:
                t = TransportHuman.objects.get(user=new_user)
            except TransportHuman.DoesNotExist:
                t = TransportHuman()
                t.user = new_user
            t.capacity = request.POST['capacity']
            t.save()
            return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                      'cat': new_user.category,
                                                      'food': food,
                                                      'water': water,
                                                      'firstaid': firstaid,
                                                      'rescuetool': rescuetools,
                                                      'fireengine': fireengine,
                                                      'jcb': jcb,
                                                      'ambulance': ambulance,
                                                      'tgoods': tgoods,
                                                      'thuman': t.capacity,
                                                      'category': json.dumps(cate)
                                                      })

    if "submitaid" in request.POST:
        v = Volunteer.objects.get(user=new_user)
        v.humanaid=request.POST['humanaid']
        v.save()
        return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                  'cat': new_user.category,
                                                  'food': food,
                                                  'water': water,
                                                  'firstaid': firstaid,
                                                  'rescuetool': rescuetools,
                                                  'fireengine': fireengine,
                                                  'jcb': jcb,
                                                  'ambulance': ambulance,
                                                  'tgoods': tgoods,
                                                  'thuman': thuman,
                                                  'category': json.dumps(cate)
                                                  })
    if "submitcapacity" in request.POST:
        a =Accomadation.objects.get(user=new_user)
        a.capacity=request.POST['capacity']
        a.save()
        return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                  'cat': new_user.category,
                                                  'food': food,
                                                  'water': water,
                                                  'firstaid': firstaid,
                                                  'rescuetool': rescuetools,
                                                  'fireengine': fireengine,
                                                  'jcb': jcb,
                                                  'ambulance': ambulance,
                                                  'tgoods': tgoods,
                                                  'thuman': thuman,
                                                  'category': json.dumps(cate)
                                                  })
    if "submitpopulation" in request.POST:
        p =Pronearea.objects.get(user=new_user)
        p.population=request.POST['population']
        p.save()
        return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                  'cat': new_user.category,
                                                  'food': food,
                                                  'water': water,
                                                  'firstaid': firstaid,
                                                  'rescuetool': rescuetools,
                                                  'fireengine': fireengine,
                                                  'jcb': jcb,
                                                  'ambulance':ambulance,
                                                  'tgoods': tgoods,
                                                  'thuman': thuman,
                                                  'category': json.dumps(cate)
                                                  })
    if "submitcanoccupy" in request.POST:
        h =Hospital.objects.get(user=new_user)
        h.canoccupy=request.POST['canoccupy']
        h.save()
        return render(request, 'updateres.html', {'username': request.session['username'], 'req': "success",
                                                  'cat': new_user.category,
                                                  'food': food,
                                                  'water': water,
                                                  'firstaid': firstaid,
                                                  'rescuetool': rescuetools,
                                                  'fireengine': fireengine,
                                                  'jcb': jcb,
                                                  'ambulance': ambulance,
                                                  'tgoods': tgoods,
                                                  'thuman': thuman,
                                                  'category': json.dumps(cate)
                                                  })
    return render(request, 'updateres.html', {'username': request.session['username'],
                                                  'cat': new_user.category,
                                                  'food': food,
                                                  'water': water,
                                                  'firstaid': firstaid,
                                                  'rescuetool': rescuetools,
                                                  'fireengine': fireengine,
                                                  'jcb': jcb,
                                                  'ambulance': ambulance,
                                                  'tgoods': tgoods,
                                                  'thuman': thuman,
                                                   'category': json.dumps(cate)
                                                  })

def requestres(request):
    if 'username' not in request.session:
        return redirect(index)
    usr=User.objects.get(username=request.session['username'])
    if usr.category=='volunteer':
        mem=Volunteer.objects.get(user=usr)
    if usr.category == 'hospital':
        mem = Hospital.objects.get(user=usr)
    if usr.category == 'accommodation':
        mem = Accomadation.objects.get(user=usr)
    if usr.category == 'pronearea':
        mem = Pronearea.objects.get(user=usr)
    addr = mem.loyalto
    stat = mem.status
    if(stat==0):
        return render(request, 'request.html', {'username': request.session['username'], 'statuserror': "success"})
    else:
        m = Messagebox()
        if "submitfood" in request.POST:
            m.fromaddr=request.session['username']
            m.toaddr=addr
            m.topic="Request"
            m.message="Food"
            m.parameter=request.POST['food']
            m.save()
            return render(request, 'request.html', {'username': request.session['username'], 'req': "success"})
        if 'submitwater' in request.POST:
            m.fromaddr=request.session['username']
            m.toaddr=addr
            m.topic="Request"
            m.message = "Water"
            m.parameter = request.POST['water']
            m.save()
            return render(request, 'request.html', {'username': request.session['username'], 'req': "success"})
        if 'submitfirstaid' in request.POST:
            m.fromaddr=request.session['username']
            m.toaddr=addr
            m.topic="Request"
            m.message = "FirstAid"
            m.parameter = request.POST['firstaid']
            m.save()
            return render(request, 'request.html', {'username': request.session['username'], 'req': "success"})
        if 'submitrescue' in request.POST:
            m.fromaddr=request.session['username']
            m.toaddr=addr
            m.topic="Request"
            m.message = "Rescue"
            m.parameter = request.POST['rescue']
            m.save()
            return render(request, 'request.html', {'username': request.session['username'], 'req': "success"})
        if 'submitmachine' in request.POST:
            m.fromaddr=request.session['username']
            m.toaddr=addr
            m.topic="Request"
            if'fireengine' in request.POST:
                m.message = "Machine"
                m.parameter = request.POST['fireengine']
                m.save()
            if'ambulance' in request.POST:
                m.message = "Machine"
                m.parameter = request.POST['ambulance']
                m.save()
            if'jcb' in request.POST:
                m.message = "Machine"
                m.parameter=request.POST['jcb']
                m.save()
            return render(request, 'request.html', {'username': request.session['username'],'req':"success"})
        else:
            return render(request, 'request.html', {'username': request.session['username']})

def messages(request):
    if 'username' not in request.session:
        return redirect(index)
    try:
        if 'ack' in request.POST:
            inboxobj=Messagebox.objects.get(id=request.POST['ack'])
            inboxobj.ack=1
            inboxobj.save()
        if 'nack' in request.POST:
            inboxobj=Messagebox.objects.get(id=request.POST['nack'])
            inboxobj.nack=1
            inboxobj.save()
        inbox=Messagebox.objects.filter(toaddr=request.session['username'],nack=0,ack=0)
        return render(request, 'inbox.html', {'username': request.session['username'],
                                              'inbox':inbox
                                            })
    except Messagebox.DoesNotExist:
        return render(request, 'inbox.html', {'username': request.session['username']})

def outbox(request):
    if 'username' not in request.session:
        return redirect(index)
    try:

        inbox=Messagebox.objects.filter(fromaddr=request.session['username'])
        return render(request, 'outbox.html', {'username': request.session['username'],
                                              'inbox':inbox
                                            })
    except Messagebox.DoesNotExist:
        return render(request, 'outbox.html', {'username': request.session['username']})