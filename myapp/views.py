from django.http import HttpResponse
from django.shortcuts import render, redirect
from myapp.forms import appadd, imageadd
from .models import AppLib, MasterTaskHolder
from django.contrib.auth import *
from django.contrib.auth import login as loginUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.


def home(request):
    logout(request)
    return render(request, 'index.html')


def login(request):
    logout(request)
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form": form1
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('loghome')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)


def signup(request):
    logout(request)
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html', context=context)


@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def loghome(request):
    if request.user.is_authenticated:
        user = request.user
        apps = MasterTaskHolder.objects.filter(user=user)
        totalpoints = 0
        for app in apps:
            if (app.status == 'C'):
                totalpoints += app.point
        context = {
            "user": user
        }
        print(context)
        return render(request, 'loghome.html', context={"user": user, 'pointhit': totalpoints})


@login_required(login_url='login')
def tasks(request):
    if request.user.is_authenticated:
        user = request.user
        apps = MasterTaskHolder.objects.filter(user=user)
        form = imageadd(request.POST)
        totalpoints = 0
        for app in apps:
            if (app.status == 'C'):
                totalpoints += app.point
        return render(request, 'tasks.html', context={'apps': apps, 'pointhit': totalpoints, 'image': imageadd})


@login_required(login_url='login')
def addimage(request, id):
    form = imageadd(request.POST, files=request.FILES)
    if request.method == "POST":
        user = request.user
        a = MasterTaskHolder.objects.get(pk=id)
        if (a.user == user):
            if (form.is_valid):
                a.image = request.FILES['image']
                a.status = 'C'
                MasterTaskHolder.save(a)
                return redirect('tasks')
    else:
        form = imageadd(request.POST)
        return render(request, "upload.html", context={"form": form})


def adminlogin(request):
    logout(request)
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form": form1
        }
        return render(request, 'adminlogin.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if (user.is_superuser):
                    loginUser(request, user)
                    return redirect('adminhome')
                else:

                    return redirect('login')
        else:
            context = {
                "form": form
            }
            return render(request, 'adminlogin.html', context=context)


@staff_member_required(login_url="adminlogin")
def adminhome(request):
    apps = AppLib.objects.all()
    return render(request, "adminhome.html", context={"form": appadd, "apps": apps})


@staff_member_required(login_url="adminlogin")
def addapp(request):
    print("in addapp function")
    form = appadd(request.POST)
    if (form.is_valid):
        app = form.save()
        return redirect('adminhome')
    else:
        context = {
            'form': form
        }
        return render(request, 'adminhome.html', context=context)
