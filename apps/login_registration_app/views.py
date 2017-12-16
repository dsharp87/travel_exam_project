# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

# tchen@codingdojo.com

# Create your views here.
def index(request):           
    return render(request, 'login_registration_app/index.html')

def register(request):
    
    results = User.objects.registration_validator(request.POST)
    print results
    if results[0]:
        request.session['user_id'] = results[1].id
        messages.error(request, 'Yay! You registered and are now logged in!')
        # set session variables for user.id, which is results[1]
        return redirect('/login_registration_app/travels')
    else:
        for key, error_message in results[1].iteritems():
            messages.error(request, error_message, extra_tags=key)
        return redirect('/login_registration_app/')

def login(request):
    results = User.objects.login_validator(request.POST)
    if results[0]:
        request.session['user_id'] = results[1].id
        messages.error(request, 'Yay! You are now logged in!')
        # set session variables for user.id, which is results[1]
        return redirect('/login_registration_app/travels')
    else:
        for key, error_message in results[1].iteritems():
            messages.error(request, error_message, extra_tags=key)
        return redirect('/login_registration_app/')

# -------------------------------------------------------------------------------------------------------
#THIS WOULD GO IN A NEW APP
def logout(request):
    request.session.flush()
    return redirect ('/login_registration_app')

def travels(request):
    print "im displaying all travels"
    # add validation for logged in user or not
    if 'user_id' not in request.session:
        messages.error(request, 'please log in before viewing pages')
        return redirect('/login_registration_app/')
    logged_user = User.objects.get(id = request.session['user_id'])
    my_trips = logged_user.joined_trips.all()  # this needs to be joined_trips.all()
    all_trips = Trip.objects.all()     
    available_trips = all_trips.difference(my_trips)

    context = {
        'logged_user' : logged_user,
        'my_trips' : my_trips,
        'available_trips' : available_trips
    }
    
    return render(request, 'login_registration_app/travels.html', context)

def add_trip_form(request):
    print "im add trip form"
    # add validation for logged in user or not
    if 'user_id' not in request.session:
        messages.error(request, 'please log in before viewing pages')
        return redirect('/login_registration_app/')
    return render(request, 'login_registration_app/add_trip.html')

def process_new_trip(request):
    print "im processing new trip"
    print request.POST
    logged_user = User.objects.get(id = request.session['user_id'])
    results = Trip.objects.trip_validator(request.POST, logged_user)
    if results[0]:
        messages.error(request, 'Yay! You registered a new trip!')
        return redirect('/login_registration_app/travels')
    else:
        for key, error_message in results[1].iteritems():
            messages.error(request, error_message, extra_tags=key)
    return redirect ('/login_registration_app/travels/add_trip_form')

def show_trip(request, trip_id):
    print "im displaying trip info"
    # add validation for logged in user or not
    if 'user_id' not in request.session:
        messages.error(request, 'please log in before viewing pages')
        return redirect('/login_registration_app/')
    this_trip = Trip.objects.get(id = trip_id)
    print this_trip
    joined_list = this_trip.joined_list.all().exclude(name = this_trip.planned_by.name)
    print joined_list
    context = {
        'this_trip' : this_trip,
        'joined_list' : joined_list
    }
    return render(request, 'login_registration_app/trip_show.html', context)

def join_this_trip(request, trip_id):
    print "im joining this trip"
    logged_user = User.objects.get(id = request.session['user_id']) 
    this_trip = Trip.objects.get(id = trip_id)
    logged_user.joined_trips.add(this_trip) # this adds the trip object to the users "joined trips field"
    this_trip.joined_list.add(logged_user) # this adds the logged user to the trips "joined_list"
    return redirect('/login_registration_app/travels')




