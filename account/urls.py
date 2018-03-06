from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^logout/', views.logout, name='logout'),
    url(r'^$', views.landinpage, name='landinpage'),
    url(r'^messages',views.messages,name='messages'),
    url(r'^updateres',views.updateresources,name='update'),
    url(r'^outbox', views.outbox, name='outbox'),
    url(r'^requestres', views.requestres, name='request'),
    #url(r'^test/',TemplateView.as_view(template_name = 'test.html')),
    ]
