from rest_framework import serializers
from academic.models import Sender, Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message', 'subject', 'creation_date', 'read_by_receiver')


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = []


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sender
        fields = ('user')