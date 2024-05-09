from djongo import models
from user.models import User

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.PositiveIntegerField(unique=True)

    class Meta:
        app_label = 'verification'

    def __str__(self):
        return f"{self.code} for {self.user.username}"

    def _id(self):
        return f"{self._id}"
    @property
    def serialized_data(self):
        return {
            '_id': str(self.pk),  # Convert ObjectId to string
            'code': self.code,
            'user_id': str(self.user.pk),  # Convert ObjectId to string
            'username': self.user.username  # Add any other user data you need
        }
