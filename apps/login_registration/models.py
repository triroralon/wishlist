from django.db import models
from datetime import date
from django.utils.dateparse import parse_date
import re
import bcrypt


class mr_manager(models.Manager):

    def create_user(self, postData):
        fn = postData['first_name']
        ln = postData['last_name']
        email = postData['email']
        password = postData['password']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User.objects.create()
        new_user.first_name = fn
        new_user.last_name = ln
        new_user.email = email
        new_user.password = hashed_pw
        new_user.save()
        return

    def validate_new_user(self, postData):
        errors = {}
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        fn = postData['first_name']
        ln = postData['last_name']
        em = postData['email']
        pw = postData['password']
        cn = postData['confirm-password']
        if len(fn) < 2:
            errors['first_name'] = "fist name must be 2+ chars"
        if len(ln) < 2:
            errors['last_name'] = "last name must be 2+ chars"
        match = re.match(email_regex, em)
        if not match:
            errors['email'] = "valid email check"
        if User.objects.filter(email=em):
            errors['email'] = 'email not unique'
        if len(pw) < 3:
            errors['password'] = "password too short"
        if pw != cn:
            errors['confirm'] = "passwords do not match"
        return errors

    def validate_login(self, postData):
        em = postData['log_email']
        pw = postData['log_password']
        errors = {}
        user = User.objects.filter(email=em)
        if not user:
            errors['log_email'] = "email not registed"
        else:
            print(user)
            if not bcrypt.checkpw(pw.encode(), user[0].password.encode()):
                errors['log_email'] = 'password/login does not match'
        print(errors)
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateField(auto_now=True)
    objects = mr_manager()
