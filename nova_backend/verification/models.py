from djongo import models
from user.models import User

class VerificationCode(models.Model):
    email = models.EmailField(unique=True)
    code = models.PositiveIntegerField(unique=True)

    class Meta:
        app_label = 'verification'

    def __str__(self):
        return f"{self.code} for {self.user.username}"

    def _id(self):
        return f"{self._id}"
