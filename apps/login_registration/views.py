from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages


def index(request):
    if request.method == 'GET':
        context = {
            'users': User.objects.all(),
        }
        return render(request, "login_registration/index.html")


def register(request):
    errors = User.objects.validate_new_user(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")
    User.objects.create_user(request.POST)
    # messages.sucess(request, "User successfully registed")
    return redirect('/')


def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')
    else:
        em = request.POST['log_email']
        request.session['user_id'] = User.objects.get(email=em).id
        return redirect('/belt/dashboard')
