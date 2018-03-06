from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^home/', include('home.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^controlunit/', include('controlunit.urls')),
    url(r'^admin/', admin.site.urls),
    ]
