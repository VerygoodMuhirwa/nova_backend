# Generated by Django 5.0.1 on 2024-06-05 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verificationcode',
            name='user',
        ),
        migrations.AddField(
            model_name='verificationcode',
            name='email',
            field=models.EmailField(default=123, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
