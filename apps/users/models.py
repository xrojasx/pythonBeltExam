from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = []
        # This section is to validate all the users input information to register
        if len(postData['name']) < 2: 
            errors.append ("Name should be more than 2 characters")
        if len(postData['alias']) < 2:
            errors.append ("alias name should be more than 2 characters")
        if len(postData['password']) < 8:
            errors.append ("Password should be more than 8 characters")            
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append ("Email already registered")
        if not re.match(NAME_REGEX, postData['name']):
            errors.append('Name field must be letter characters only')
        if not re.match(NAME_REGEX, postData['alias']):
            errors.append('alias field must be letter characters only')
        if not re.match(EMAIL_REGEX, postData['email']):
            errors.append("invalid email")
        if postData['password'] != postData['password_confirm']:
            errors.append("passwords do not match")
        if not errors:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))
            new_user = self.create(
                name=postData['name'],
                alias=postData['alias'],
                email=postData['email'],
                dob=postData['dob'],
                password=hashed
            )
            return new_user
        return errors
    def login_validator(self, postData):
        errors = []
        #This sections is to validate the users input for login
        if len(self.filter(email=postData['email'])) > 0:
            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('email and/or password incorrect')
        else:
            errors.append('email and/or password incorrect')

        if errors:
            return errors
        return user
            
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    dob = models.DateField(max_length=8, null=True, blank=True)
    favorite = models.ManyToManyField("Quote", related_name="favorite", default=None)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class QuoteManager(models.Manager):
    def validate_quote(self, post_data):

        valid = True
        errors = []

        if len(post_data.get('content')) < 11:
            valid = False
            errors.append('Message must be more than 10 characters')
        if len(post_data.get('author')) < 3:
            valid = False
            errors.append('Author name must be more than 2 characters')
        return (valid, errors)

class Quote(models.Model):
    content = models.TextField(max_length=1000)
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="posted_by", default=None)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = QuoteManager()