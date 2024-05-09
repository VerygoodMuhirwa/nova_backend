from djongo import models

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    photo = models.CharField(max_length=255, default='https://icon-library.com/images/anonymous-avatar-icon/anonymous-avatar-icon-25.jpg')
    phoneNumber = models.CharField(max_length=255)
    def __str__(self):
        return self.email
