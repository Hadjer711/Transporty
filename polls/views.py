from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.http import HttpResponse
from .models import AnnonceMarchandise, AnnonceTrajet, User, Affectation
from .forms import AnnonceMarchandiseForm,AnnonceTrajetForm, RegisterForm, Negociation



def index(request):
    return HttpResponse("Hello, world. You're at the css index.")

def welcome(request):
    return render(request, template_name='accueil.html')



@login_required
def marchandisesave(request):
    form = AnnonceMarchandiseForm(request.POST or None)
    if form.is_valid():
        form.save(user=request.user, commit=False)
        form = AnnonceMarchandiseForm()
        print('data valid')
    else:
        print('data is not valid')
    context = {'form': form}
    template_name = 'annonceMarchandise.html'
    return render(request, template_name, context)

@login_required
def trajetsave(request):
    form = AnnonceTrajetForm(request.POST or None)
    if form.is_valid():
        form.save(user=request.user, commit=False)
        form = AnnonceTrajetForm()
        print('data valid')
    else:
        print('data is not valid')
    context = {'form': form}
    template_name = 'annonceTrajet.html'
    return render(request, template_name, context)

def register(request):
    if request.method== 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            print('data valid')
            return redirect('welcome')
    else:
        form= RegisterForm()
    context = {'form': form}
    template_name = 'register.html'
    return render(request, template_name, context)




def mylogin(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def contact(request):
    template_name='contact.html'
    return  render(request, template_name)

def compte(request):
    template_name='compte.html'
    return  render(request, template_name)

def localisation(request):
    template_name='tracking.html'
    return  render(request, template_name)

def demandes(request):
    data=AnnonceMarchandise.objects.all().filter(user=request.user)
    template_name='historiqueclient.html'
    form= Negociation()
    return  render(request, template_name,context={'data': data, 'form':form})

def trajets(request):
    data=AnnonceTrajet.objects.all().filter(user=request.user)
    template_name='historiqueTransporteur.html'
    return  render(request, template_name,context={'data': data})

def logout_view(request):
    logout(request)
    return redirect('welcome')

def negociation(request, id):
    if request.method == 'POST':
        tarif = request.POST['tarif']
        Affectation.objects.filter(pk=id).update(tarif=tarif)
        AnnonceMarchandise.objects.filter(pk=id).update(tarif=tarif)
        AnnonceTrajet.objects.filter(pk=id).update(tarif=tarif)
        print(tarif)
    data = AnnonceMarchandise.objects.all().filter(user=request.user)
    template_name = 'historiqueclient.html'
    form = Negociation()
    return render(request, template_name, context={'data': data, 'form': form})

