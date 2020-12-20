from django.shortcuts import render, redirect, HttpResponse
from .models import User, Quote
from django.contrib import messages
import bcrypt

import itertools
import functools


def index(request):
    print('*'*80)
    print("in the index method")
    if 'user' in request.session:    
        del request.session['user']
    return render (request, 'quotes_app/index.html')

def register(request):
    print('*'*80)
    print("in the register method")
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        else:
            password=request.POST['password']
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash.decode())
            request.session['user']=request.POST['first_name']
            request.session['user_id']=new_user.id
            return redirect ('/quotes')
    return redirect ('/')

def login(request):
    print('*'*80)
    print("in the login method")
    if request.method =='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user=User.objects.filter(email=request.POST['email'])
            logged_user=user[0]
            request.session['user'] = logged_user.first_name
            request.session['user_id']=logged_user.id
            return redirect ('/quotes')
    else:
        return redirect ('/')


def edit_user(request):
    print('*'*80)
    print("in the edit method")
    if request.method =='POST':
        errors = User.objects.update_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        else:
            user_to_update = User.objects.get(id = request.POST['thisuser'])
            user_to_update.first_name = request.POST['first_name']
            user_to_update.last_name = request.POST['last_name']
            user_to_update.email = request.POST['email']
            user_to_update.save()
            request.session['user']=request.POST['first_name']
            request.session['user_id']= request.POST['thisuser']
            return redirect ('/quotes')
    return redirect ('/')

def edit(request, user_id):
    print('*'*80)
    print("in the quote_id method")
    print("liked", User.objects.filter(id=request.session['user_id'])) 
    context = {
        'thisuser': user_id,
    }
    return render (request, 'quotes_app/edit_user.html', context)


def quotes(request):
    print('*'*80)
    print("in the quote_id method")
    print("liked", User.objects.filter(id=request.session['user_id'])) 
    
    context = {
        'allqoutes' : Quote.objects.all(),
        'addedby' : Quote.objects.first(),
        'liked' : User.objects.filter(id=request.session['user_id']).first().liked_quotes.all(),
        'allusers':User.objects.all(),
        'counter': functools.partial(next, itertools.count()),
    }
    
    return render (request, 'quotes_app/quotes.html', context)


def quotes_id(request, quote_id):
    print('*'*80)
    print("in the quote_id method")
    thisuser=Quote.objects.get(id=quote_id).user_who_like.all()
    thisquote=Quote.objects.get(id=quote_id)
    likedthisquote=Quote.objects.get(id=quote_id).user_who_like.filter(id=request.session['user_id'])
    context = {
        'thisuser' : thisuser,
        'thisquote' : thisquote,
        'likedthisquote': likedthisquote,
    }
    return render (request, 'quotes_app/quotes_id.html', context)

def user_quotes(request, user_id):
    print('*'*80)
    print("in the quote_id method")
    context = {
        'allqoutes' : Quote.objects.all(),
        'addedby' : Quote.objects.first(),
        'liked' : User.objects.filter(id=request.session['user_id']).first().liked_quotes.all()
    }
    return render (request, 'quotes_app/user_quotes.html', context)

def quotes_ad(request):
    print('*'*80)
    print("in the quotes_ad method")
    if request.method =='POST':
        errors = User.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quotes')
        else: 
            user_id=request.session['user_id']
            quoteobject=Quote.objects.create(author=request.POST['title'], description=request.POST['description'], uploaded_by=User.objects.get(id=user_id))
            this_user=User.objects.get(id=user_id)
            quoteid=quoteobject.id
            quoteobject.user_who_like.add(this_user)
            return redirect ('/quotes') #/quotes/'+str(quoteid))

def quotes_id_update(request, quote_id):
    print('*'*80)
    print("in the books_id_update method")
    if request.method =='POST': 
        updates=Quote.objects.get(id=quote_id)
        updates.author=request.POST['title']
        updates.description=request.POST['description']
        updates.save()
        return redirect ('/quotes/'+quote_id)
    else:
        return redirect ('/quotes')


def favorite(request, quote_id):
    print('*'*80)
    print("in the favorite method")
    user_id=request.session['user_id']
    quoteobject=Quote.objects.get(id=quote_id)
    this_user=User.objects.get(id=user_id)
    quoteobject.user_who_like.add(this_user)
    return redirect ('/quotes')


def unfavorite(request, quote_id):
    print('*'*80)
    print("in the unfavorite method")
    user_id=request.session['user_id']
    quoteobject=Quote.objects.get(id=quote_id)
    this_user=User.objects.get(id=user_id)
    quoteobject.user_who_like.remove(this_user)
    return redirect ('/quotes')

def destroy(request, quote_id):
    print('*'*80)
    print("in the destroy method")
    deleted=Quote.objects.get(id=quote_id)
    deleted.delete()
    return redirect ('/quotes')

def quotes_id_edit(request, quote_id):
    print('*'*80)
    print("in the edit method")
    thisquote=Quote.objects.get(id=quote_id)
    context = {
        'thisquote' : thisquote
    }
    return render (request, 'quotes_app/quote_id_edit.html', context)
