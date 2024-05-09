from rest_framework import serializers
from .models import VerificationCode

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

class VerificationCodeSerializer(serializers.ModelSerializer):
    object_id = ObjectIdField(source='id')  # Assuming 'id' is the ObjectId field

    class Meta:
        model = VerificationCode
        fields = ['object_id', 'code']  # Include other fields as needed
