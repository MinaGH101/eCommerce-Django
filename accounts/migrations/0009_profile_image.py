# Generated by Django 4.1.6 on 2023-05-05 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_alter_profile_phone_alter_profile_postal_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                blank=True, default=None, null=True, upload_to="images"
            ),
        ),
    ]
