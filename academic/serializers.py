from rest_framework import serializers
from academic.models import Message, Sender, Message1


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('sender', 'receiver', 'message', 'subject', 'creation_date')


class Message1Serializer(serializers.ModelSerializer):

    class Meta:
        model = Message1
        fields = ('sender', 'receiver', 'message', 'subject', 'creation_date','read_by_receiver')


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = []


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sender
        fields = ('user')