# Generated by Django 3.0.3 on 2024-10-08 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0002_remove_verificationcode_user_verificationcode_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VerificationCode',
        ),
    ]
