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
    return redirect('/quotes')

def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "You are logged in!")
    return redirect('/quotes')

def user(request, id):
	user =  User.objects.get(id = id)
	context = {
		'user': user,
		'quotes': user.posted_by.all()		
	}
	return render(request, 'users/show.html', context)

def quotes(request):
	user = current_user(request)
	context = {
		'user': user,
		'quotable_quotes': Quote.objects.exclude(favorite = user),
		'favorite': user.favorite.all()
	}
	return render(request, 'users/success.html', context)

def success(request):
    if request.method != 'POST':
		return redirect('/')
	
    check = Quote.objects.validate_quote(request.POST)
    if request.method != 'POST':
		return redirect('/quotes')
    if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="add_item")
			return redirect('/quotes')
    if check[0] == True:

		quote = Quote.objects.create(
			content = request.POST.get('content'),
			user = current_user(request),
			author = request.POST.get('author')
			)

		return redirect('/quotes')
    return redirect('/quotes')

def addfav(request, id):
	user = current_user(request)
	favorite = Quote.objects.get(id=id)

	user.favorite.add(favorite)

	return redirect('/quotes')

def removefav(request, id):
	user = current_user(request)
	favorite = Quote.objects.get(id=id)

	user.favorite.remove(favorite)

	return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect('/')

