from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, default=None ,on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    phone = models.CharField(max_length=50,default=None, blank=True, null=True)
    address1 = models.CharField(max_length=50, default=None, blank=True, null=True)
    address2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    state = models.CharField(max_length=50, default=None, blank=True, null=True)
    area = models.CharField(max_length=50, default=None, blank=True, null=True)
    postal_code = models.CharField(max_length=50,default=None, blank=True, null=True)
    image = models.ImageField(upload_to='images', default=None, blank=True, null=True)


