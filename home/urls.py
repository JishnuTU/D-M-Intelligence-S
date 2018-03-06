from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^$',views.index,name='index'),
    url(r'^test/',TemplateView.as_view(template_name = 'test.html')),
    ]
