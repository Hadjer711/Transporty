"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from polls import views
from polls.views import welcome,  marchandisesave, trajetsave,register,localisation, mylogin, compte,contact, logout_view, demandes, trajets, negociation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('welcome/', welcome, name='welcome'),
    path('marchandise/', marchandisesave, name='marchandise'),
    path('trajet/', trajetsave, name='trajet'),
    path('register/', register, name='register'),
    path ('login/',mylogin, name='login'),

    path('contact/',contact, name='contact'),
    path('compte/',compte, name='compte'),
    path('logout/', logout_view, name='logout'),
path('demandes/', demandes, name='demande'),
path('trajets/', trajets, name='trajets'),
path('localisation/', localisation, name='localisation'),
path('negociation/<int:id>', negociation, name='negocier'),
]





