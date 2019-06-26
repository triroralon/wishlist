from django.shortcuts import render, redirect, HttpResponse
from apps.login_registration.models import User
from django.contrib import messages
from .models import *
from datetime import date


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['user_id'])
    user_id = request.session['user_id']
    # number = len(likes.Wish.all())
    context = {
        'user_id': request.session['user_id'],
        'user': User.objects.get(id=user_id),
        'wish': Wish.objects.all(),
    }
    return render(request, 'belt/dashboard.html', context)


def new_wish(request):
    user = User.objects.get(id=request.session['user_id'])
    user_id = request.session['user_id']
    context = {
        'user_id': request.session['user_id'],
        'user': User.objects.get(id=user_id),
    }
    if 'user_id' not in request.session:
        return redirect("/")
    if request.method == "GET":
        print("here")
        return render(request, 'belt/new_wish.html', context)
    print("*"*25)
    errors = Wish.objects.validate_wish(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/belt/new")
    new_wish = Wish.objects.create(
        item=request.POST['item'],
        description=request.POST['description'],
        wish_creator=user
    )
    print(user)
    return redirect("/belt/dashboard", context)


def granted(request):
    if 'user_id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['user_id'])
    w = Wish.objects.get(id=request.POST['wish_id'])
    w.wish_granted = user
    w.wish_granted_at = date.today()
    w.save()
    return redirect("/belt/dashboard")


def delete(request):
    if 'user_id' not in request.session:
        return redirect("/")
    wish_id = request.POST['wish_id']
    wish = Wish.objects.get(id=wish_id)
    wish.delete()
    return redirect('/belt/dashboard')


def edit(request):
    if 'user_id' not in request.session:
        return redirect("/")
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'wish_id': request.POST['wish_id'],
            'wish': Wish.objects.get(id=request.POST['wish_id']),
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'belt/edit.html', context)


def process_edit(request):
    if 'user_id' not in request.session:
        return redirect("/")
    errors = Wish.objects.validate_wish(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return edit(request)
    w = Wish.objects.get(id=request.POST['wish_id'])
    w.item = request.POST['item']
    w.description = request.POST['description']
    w.save()
    return redirect('/belt/dashboard')


def logout(request):
    request.session.flush()
    return redirect("/")


def like_wish(request):
    if 'user_id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['user_id'])
    wish = Wish.objects.get(id=request.POST['wish_id'])
    wish.likes.add(user)
    return redirect('/belt/dashboard')


def stats(request):
    if 'user_id' not in request.session:
        return redirect("/")
    user = User.objects.get(id=request.session['user_id'])
    user_id = request.session["user_id"]
    wish = Wish.objects.all()

    context = {
        "user_id": request.session['user_id'],
        'wish': wish,
        'user': user,
        'pending': Wish.objects.filter(wish_granted__isnull=True).filter(wish_creator=user_id).count(),
        'all': Wish.objects.exclude(wish_granted__isnull=True).count(),
        'granted': Wish.objects.filter(wish_granted=user_id).count(),
    }
    return render(request, 'belt/stats.html', context)
