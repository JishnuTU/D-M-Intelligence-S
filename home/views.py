from django.shortcuts import render, redirect
from models import User
from account.models import  Volunteer,Accomadation,Hospital,Pronearea

from account.views import landinpage
from controlunit.views import cplandinpage

from tests import index


def register(request):

    if request.method == 'POST' and 'register' in request.POST:
        try:
            existing_user= User.objects.get(username = request.POST['username'])
            return render(request, 'register.html', {"fail" : "failed"})

        except User.DoesNotExist:
            new_user=User()
            new_user.username=request.POST['username']
            new_user.password=request.POST['pwd']
            new_user.category=request.POST['category']
            new_user.location =request.POST['lname']
            new_user.longitude = request.POST['ll']
            new_user.latitude =request.POST['la']
            new_user.email = request.POST['email']
            new_user.contact_no =request.POST['contactno']

            if(request.POST['category']=='volunteer'):
                new_vol=Volunteer()
                new_vol.user=new_user
                new_vol.name= request.POST['name']
                new_vol.usertype=request.POST['atype']
                new_vol.save()

            if (request.POST['category'] == 'hospital'):
                new_hos = Hospital()
                new_hos.user = new_user
                new_hos.name = request.POST['name']
                new_hos.usertype = request.POST['atype']
                new_hos.save()

            if (request.POST['category'] == 'accommodation'):
                new_acc = Accomadation()
                new_acc.user = new_user
                new_acc.name = request.POST['name']
                new_acc.usertype = request.POST['atype']
                new_acc.save()

            if (request.POST['category'] == 'pronearea'):
                new_parea = Pronearea()
                new_parea.user = new_user
                new_parea.name = request.POST['name']
                new_parea.usertype = request.POST['atype']
                new_parea.save()
            new_user.save()
            return render(request, 'register.html', {"status":"success"})
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST' and 'login' in request.POST:
        try:
            ob = User.objects.get(username=request.POST['username'], password=request.POST['pwd'])
            if ob.category=='controlunit':
                request.session['cusername'] = request.POST['username']
                return redirect(cplandinpage)
            else:
                request.session['username'] = request.POST['username']
                return redirect(landinpage)
        except User.DoesNotExist:
            return render(request, 'login.html',{"status":"Failed"})
    else:
        return render(request, 'login.html')