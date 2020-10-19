from rest_framework import serializers
from academic.models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('sender', 'receiver', 'message', 'subject', 'creation_date')