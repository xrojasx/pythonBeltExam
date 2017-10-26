from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, 'users/index.html')

def current_user(request):
	return User.objects.get(id=request.session['user_id'])

def register(request):
    result = User.objects.registration_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "You are now registered!")
    return redirect('/travel')

def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "You are logged in!")
    return redirect('/travel')

def travel(request):
    user = current_user(request)
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "travels" : Trip.objects.all(),
        "others": Trip.objects.all().exclude(join__id=request.session['user_id'])
    }
    return render(request, 'users/success.html', context)

def addtrip(request):
    context= {
        "user":User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'users/addtrip.html', context)

def createtrip(request):
    if request.method != 'POST':
        return redirect ("/addtrip")
    newtrip= Trip.objects.new_trip(request.POST, request.session["user_id"])
    if newtrip[0] == True:
        return redirect('/travel')
    else:
        for message in newtrip[1]:
            messages.error(request, message)
        return redirect('/addtrip')

def show(request, trip_id):
    try:
        trip= Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        messages.info(request,"Travel Not Found")
        return redirect('/travel')
    context={
        "trip": trip,
        "user":User.objects.get(id=request.session['user_id']),
        "others": User.objects.filter(joiner__id=trip.id).exclude(id=trip.creator.id),
    }
    return render(request, 'users/show.html', context)

def join(request, trip_id):
    if request.method == "GET":
        messages.error(request,"What trip?")
        return redirect('/')
    joiner= Trip.objects.join(request.session["user_id"], trip_id)
    if 'errors' in joiner:
        messages.error(request, joiner['errors'])
    return redirect('/travel')

def delete(request, id):
    try:
        target= Trip.objects.get(id=id)
    except Trip.DoesNotExist:
        messages.info(request,"Message Not Found")
        return redirect('/travel')
    target.delete()
    return redirect('/travel')

def logout(request):
    request.session.clear()
    return redirect('/')

