"""test_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from clinic.views import search, add_patient_view, list_appointment_view, appointment_view, details, add_record_view, \
    recup, docup, home, dochome, rechome

urlpatterns = [

    path('admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^docup/$',docup, name="docer"),
    url(r'^recup/$',recup, name="recer"),
    url(r'^addp/$',add_patient_view, name="addp"),
    url(r'^home/$',home, name="home"),
    url(r'^$',home, name="home"),
    url(r'^appointments/$', list_appointment_view, name='appointments'),
    url(r'^search/$', search, name='search'),
    url(r'^appointment/$', appointment_view, name='appointment'),
    url(r'^patients/(?P<pk>\d+)/$', details, name='details'),
    url(r'^addrec/(?P<pk>\d+)/$', add_record_view ,name='addrec'),
    url(r'^dochom/$',dochome, name="dochome"),
    url(r'^rechom/$',rechome, name="rechome"),

]
