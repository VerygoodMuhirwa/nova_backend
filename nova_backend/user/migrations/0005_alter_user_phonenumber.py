# Generated by Django 5.0.1 on 2024-06-05 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phoneNumber',
            field=models.CharField(max_length=255),
        ),
    ]