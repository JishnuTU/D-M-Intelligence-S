from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    #url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^systempanel',views.controlpanel,name='panel'),
    url(r'^$', views.cplandinpage, name='cplandinpage'),
    url(r'^nearestlocater',views.servicelocater,name='locater'),
    url(r'^responsebox',views.responsebox,name='responsebox'),
    url(r'^messages',views.cpmessages,name='messages'),
    ]
