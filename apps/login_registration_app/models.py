# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name_length"] = "First Name must be at least three characters"
        if not postData['name'].isalpha():
            errors["name_alpha"] = "Your First Name can be only letters(no numbers, spaces, or symbols)"
        if len(postData['username']) < 3:
            errors["username_length"] = "Username must be at least three characters"
        if not postData['username'].isalpha():
            errors["username_alpha"] = "Your userame can be only letters(no numbers, spaces, or symbols)"
        if User.objects.filter(username = postData['username']):
            errors['username_exists'] = "We haz a username called this already"
        if len(postData['password']) < 8:
            errors["password_length"] = "Password must be at least 8 characters" 
        if not postData['password'].isalpha():
            errors["password_chars"] = 'Password must contain only alphanumeric characters'
        if not postData['password'] == postData['password_comfirmation']:
            errors['email_confirmation'] = "Password Confirmation must match Password"
        
        if len(errors):
            print "i failed"
            return (False, errors)
        else:
            print "i passed"
            hash_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = self.create(name = postData['name'], username = postData['username'], password = hash_pw)
            return (True, user)

    def login_validator(self, postData):
        errors = {}
        attempt_user = User.objects.filter(username = postData['username'])
        if len(attempt_user) == 0:
            errors['not_found'] = 'we do not have a user with this username on reccord'
            return (False, errors)
        elif len(attempt_user) > 1:
            errors['dupes'] = 'we have multiple accounts with this username....HOW DO??!?!'
            return (False, errors)
        else:
            print attempt_user[0].password
            print bcrypt.checkpw(postData['password'].encode(),attempt_user[0].password.encode())
            if bcrypt.checkpw(postData['password'].encode(), attempt_user[0].password.encode()):
                return (True, attempt_user[0])
            else:
                errors['pw_fail'] = 'your password is incorrect NOOB'
                return(False, errors)
# -------------------------------------------------------------------------------------------

class TripManager(models.Manager):
    def trip_validator(self, postData, logged_user):
        errors = {}
        if len(postData['destination']) < 1:
            errors["destination_length"] = "Your desintation must be at least one character"
        if len(postData['activity']) < 1:
            errors["activity_length"] = "Your descrition must be at least one character"
        if datetime.datetime.now().strftime('%Y-%m-%d') > postData['startdate']:
            errors["startdate_past"] = "Your start date must be in the future"
        if datetime.datetime.now().strftime('%Y-%m-%d') > postData['enddate']:
            errors["enddate_past"] = "Your end date must be in the future"
        if postData['startdate'] > postData['enddate']:
            errors["end_before_start"] = "Your end date must be after your start "
        if len(errors):
            print "i failed"
            return (False, errors)
        else:
            print "i passed"
            new_trip = self.create(destination = postData['destination'], activity = postData['activity'], startdate = postData['startdate'], enddate = postData['enddate'], planned_by = logged_user)
            logged_user.joined_trips.add(new_trip) # this adds the newly created trip to the user who created it's joined trips field
            return (True, new_trip)
        


# ***********************************************************************************************************

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    activity = models.CharField(max_length=255)
    startdate = models.DateField()
    enddate = models.DateField()
    planned_by = models.ForeignKey(User, related_name = "trips")
    joined_list = models.ManyToManyField(User, related_name="joined_trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()

