from django.db import models
from apps.login_registration.models import User
from datetime import date
from django.utils.dateparse import parse_date


class wish_manager(models.Manager):

    # def create_wish(self, postData):
    #     user = User.objects.get(id=postData.session['user_id'])
    #     new_trip = Trip.objects.create(
    #         item=postData['item'],
    #         description=postData['desctiption'],
    #         wish_creator=user
    #     )
    #     return

    def edit_wish(self, postData):
        new_trip = Trip.objects.create()
        new_trip.save()
        return

    def validate_wish(self, postData):
        errors = {}
        item = postData['item']
        description = postData['description']
        if len(item) < 3:
            errors['destination'] = "Please enter a item"
        if len(description) < 3:
            errors['descripting'] = "Please enter an description"
        return errors


class Wish(models.Model):
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateField(auto_now=True)
    wish_creator = models.ForeignKey(User, related_name="wish_creator")
    wish_granted = models.ForeignKey(User, related_name="wish_granted", null=True)
    wish_granted_at = models.DateField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="likes")
    update_at = models.DateTimeField(auto_now=True)
    objects = wish_manager()


class Likes(models.Model):
    liker = models.ForeignKey(User, related_name="liker")
    wish_liked = models.ForeignKey(Wish, related_name="wish_liked")
    created_at = models.DateField(auto_now=True)
