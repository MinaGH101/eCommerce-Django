# Generated by Django 4.1.6 on 2023-05-04 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(name="Profile",),
    ]