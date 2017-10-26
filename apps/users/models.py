from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import date, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = []
        # This section is to validate all the users input information to register
        if len(post_data['name']) < 2: 
            errors.append ("Name should be more than 2 characters")
        if len(post_data['username']) < 2:
            errors.append ("Username name should be more than 2 characters")          
        if len(User.objects.filter(username=post_data['username'])) > 0:
            errors.append ("Username already registered")
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('Name field must be letter characters only')
        if not re.match(NAME_REGEX, post_data['username']):
            errors.append('Username field must be letter characters only')
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")
        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
            new_user = self.create(
                name=post_data['name'],
                username=post_data['username'],
                password=hashed
            )
            return new_user
        return errors
    def login_validator(self, post_data):
        errors = []
        #This sections is to validate the users input for login
        if len(self.filter(username=post_data['username'])) > 0:
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Username and/or password incorrect')
        else:
            errors.append('Username and/or password incorrect')

        if errors:
            return errors
        return user
            
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, default=None)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class TripManager(models.Manager):
    def new_trip(self, post_data, id):
        errors = []
        if len(post_data['destination']) < 1:
            errors.append('Destination cannot be empty')
        if len(post_data['description']) < 1:
            errors.append('Description cannot be empty')
        if str(date.today()) > str(post_data['start']):
            errors.append("Please input a valid date. Note: Start time can not be before today.")
        if str(date.today()) > post_data['end']:
            errors.append("Please input a valid date. Note: End date must be after start date")
        if post_data['start'] > post_data['end']:
            errors.append("Travel Date From can not be in the future of Travel Date To")
        if len(errors) == 0:
            plan= Trip.objects.create(
                destination=post_data['destination'],
                description=post_data['description'], 
                start=post_data['start'],
                end=post_data['end'], 
                creator= User.objects.get(id=id),
                )
            return (True, plan)
        else:
            return (False, errors)

    def join(self, id, trip_id):
        if len(Trip.objects.filter(id=trip_id).filter(join__id=id))>0:
            return {'errors':'You already Joined this'}
        else:
            joiner= User.objects.get(id=id)
            plan= self.get(id= trip_id)
            plan.join.add(joiner)
            return {}

class Trip(models.Model):
    destination = models.CharField(max_length=255, default=None)
    start = models.DateField(default=None)
    end = models.DateField(default=None)
    description = models.TextField(max_length=1000, default=None)
    creator= models.ForeignKey(User, related_name= "planner", default=None)
    join= models.ManyToManyField(User, related_name="joiner", default=None)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = TripManager()