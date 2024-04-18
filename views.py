from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
#importujeme model ktery chceme zaradit
from .models import Mistnost, Tema, Zprava
from django.http import HttpResponse
from django.db.models import Q
from .forms import MistnostForm, UserForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('domovska')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Uživatel neexistuje.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('domovska')
        else:
            messages.error(request, 'Přihlašovací údaje se neshodují.')

    context = {'page': page}
    return render(request, 'login_registrace.html', context)


def logoutUser(request):
    logout(request)
    return redirect('domovska')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('domovska')
        else:
            messages.error(request, 'Nemohli jsme vas zaregistrovat sry')

    return render(request, 'login_registrace.html', {'form': form})


#vyvorime view na zaklade funkce, takze:
def domovska(request):
    #do teto funkce passnem data co requestujem z vyhledavani, a vratime odpoved
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    mistnosti = Mistnost.objects.filter(
        Q(tema__jmeno__icontains=q)|
        Q(jmeno__icontains=q)|
        Q(popis__icontains=q)
        )

    temata = Tema.objects.all()
    mistnost_count = mistnosti.count()
    zpravy_mistnosti = Zprava.objects.all()

    context = {'mistnosti': mistnosti, 'temata': temata, 'mistnost_count': mistnost_count, 'zpravy_mistnosti' : zpravy_mistnosti }
    #vracime se zpatky na domovskou, s kontextem (jmeno mistnosti...)
    return render(request,'domovska.html', context)


def mistnost(request,pk):
    #do teto funkce passnem data co requestujem, a vratime odpoved
    mistnost = Mistnost.objects.get(id=pk)
    zpravy_mistnosti = mistnost.zprava_set.all()#.order_by('-vytvoreno')
    ucastnici = mistnost.ucastnici.all()
    if request.method == 'POST':
        zprava = Zprava.objects.create(
            user=request.user,
            mistnost=mistnost,
            zprava=request.POST.get('zprava_body')
        )
        mistnost.ucastnici.add(request.user)
        return redirect('mistnost',pk=mistnost.id)

    context = {'mistnost': mistnost, 'zpravy_mistnosti': zpravy_mistnosti,
               'ucastnici': ucastnici }
    return render(request,'mistnost.html', context)

def userProfil(request, pk):
    user = User.objects.get(id=pk)
    mistnosti = user.mistnost_set.all()
    context = {'user': user,'mistnosti': mistnosti }
    return render(request,"profil.html", context)


@login_required(login_url='/login')
def vytvorMistnost(request):
    form = MistnostForm()
    if request.method == "POST":
        form = MistnostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('domovska')

    context = {'form': form}
    return render(request,'mistnost_form.html',context)

@login_required(login_url='/login')
def upravMistnost(request, pk):
    mistnost = Mistnost.objects.get(id=pk)
    form = MistnostForm(instance=mistnost) 

    if request.user != mistnost.host:
        return HttpResponse("Přístup odepřen")

    if request.method == "POST":
        form = MistnostForm(request.POST, instance=mistnost)
        if form.is_valid():
            form.save()
            return redirect('domovska')

    context = {'form': form}
    return render(request,'mistnost_form.html',context)

@login_required(login_url='/login')
def deleteMistnost(request, pk):

    mistnost = Mistnost.objects.get(id=pk)

    if request.user != mistnost.host:
        return redirect('domovska')

    if request.method == "POST":
        mistnost.delete()
        return redirect('domovska')
    return render(request,'delete.html',{'obj':mistnost})


@login_required(login_url='/login')
def deleteZprava(request, pk):
    zprava = Zprava.objects.get(id=pk)

    if request.user != zprava.user:
        return redirect('domovska')

    if request.method == "POST":
        zprava.delete()
        return redirect('domovska')
    return render(request,'delete.html',{'obj': zprava})

@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('domovska')                                     #pk=user.id (pro profil later)
    return render(request,'update-user.html', {'form':form})
