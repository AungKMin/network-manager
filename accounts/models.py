from django.db import models
from django.contrib.auth.models import User

"""
UserWrapper for user account
"""
class UserWrapper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self): 
        return self.user.username

"""
Tag for contact (e.g. work contact, etc)
"""
class ContactTag(models.Model):
    name = models.CharField(max_length=200, null=True)
    user_wrapper = models.ForeignKey(UserWrapper, null=True, on_delete=models.SET_NULL) 

    def __str__(self):
        return self.name

"""
Contact (a person)
"""
class Contact(models.Model):
    name = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    organization = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    contact_tags = models.ManyToManyField(ContactTag)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True)
    user_wrapper = models.ForeignKey(UserWrapper, null=True, on_delete=models.SET_NULL) 

    def __str__(self):
        return self.name

"""
Method/Type of a contact point (email, etc)
"""
class ContactPointMethod(models.Model):
    name = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    hours_for_response = models.FloatField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True) 
    user_wrapper = models.ForeignKey(UserWrapper, null=True, on_delete=models.SET_NULL) 

    def __str__(self):
        return self.name

"""
Contact point specific to a contact
"""
class ContactPoint(models.Model):
    STATUS = (
        ('None', 'None'),
        ('Sent', 'Sent'),
        ('Responded - reply', 'Responded - reply'),
        ('Responded - done', 'Responded - done'),
    )
    contact = models.ForeignKey(Contact, null=True, on_delete=models.SET_NULL) 
    contact_point_method = models.ForeignKey(ContactPointMethod, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    link = models.CharField(max_length=1000, null=True, blank=True)
    notes = models.CharField(max_length=1000, null=True, blank=True)
    times_used = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.link