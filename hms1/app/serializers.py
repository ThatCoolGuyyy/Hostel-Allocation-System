from rest_framework import serializers
from .models import *


class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'