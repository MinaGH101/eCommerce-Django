from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Message(models.Model):
    # name = models.CharField(max_length=50, blank=True, null=True, default='Enter Your First & Last name ...')
    # email = models.EmailField(max_length=100, blank=True, null=True, default='Enter Your Email ...')
    # phone_regex = RegexValidator(regex=r'^\+?98?\d{9,15}$', message="Example: +9121234567")
    # phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, default='Enter Your Phone Number ...')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_cart')
    message = models.TextField(blank=False, null=True, default='...Enter Your Message ...')
    created = models.DateTimeField(auto_now=True)
    