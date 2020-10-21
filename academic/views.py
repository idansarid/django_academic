from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from academic.models import Bulletin, User, Message
from datetime import datetime


@login_required(login_url="/login")
def index(request):
    bulletins = {'bulletins': Bulletin.objects.all()}
    return render(request, 'index.html', bulletins)


def adminlogin(request):
    return HttpResponse("Hello World IDAN")


def username(request):
    return HttpResponse("Your username is:"+request.user.username)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse("Unautorized!")
        else:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if (username == ""): return HttpResponse("No username!")
        if (password == ""): return HttpResponse("No password!")
        if (email == ""): return HttpResponse("No email!")
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse("Unautorized!")
        else:
            login(request, user)
            return redirect('/')
    return render(request, "register.html")


def logout_user(request):
    logout(request)
    return HttpResponse("Successfully logged out!")


@login_required(login_url="/login")
def dashboard(request):
    if request.method == 'POST':
        body = request.POST['body']
        bulletin = Bulletin()
        bulletin.body = body
        bulletin.save()
    if request.user is None or not request.user.is_staff:
        return HttpResponse("Unauthorized!")
    return render(request, 'admindash.html')


from academic.models import Message, Message1, User, Sender, Receiver
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from academic.serializers import MessageSerializer, UserSerializer, Message1Serializer, ListSerializer
import copy


@api_view(['GET', 'POST'])
def message_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        messages = Message1.objects.all()
        serializer = Message1Serializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def write_message(request):
    """
    List all code snippets, or create a new snippet.
    """
    users = User.objects.all()
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = Message1Serializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = Message1Serializer(data=request.data)
        message = Message1()
        message.creation_date = datetime.now
        message.sender = str(serializer.initial_data['sender'])
        message.receiver = str(serializer.initial_data['receiver'])
        message.message = str(serializer.initial_data['message'])
        message.subject = str(serializer.initial_data['subject'])
        message.save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def all_messages_for_user(request):
    """
    List all code snippets, or create a new snippet.
    """
    expected_user = request.data['user']
    users = User.objects.all()
    if request.method == 'POST':
        for user in users:
            if expected_user == user.get_username():
                messages = Message1.objects.filter(receiver=user.get_username())
                serializer = Message1Serializer(messages, many=True)
                return Response(serializer.data)
        return HttpResponse("No data for user {}".format(request.data))
    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def read_message(request):
    """
    List all code snippets, or create a new snippet.
    """
    users = User.objects.all()
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = Message1Serializer(data=request.data)
        message = Message1()
        message.creation_date = datetime.now
        message.sender = serializer.initial_data['sender']
        message.receiver = serializer.initial_data['receiver']
        message.message = serializer.initial_data['message']
        message.subject = serializer.initial_data['subject']
        message.save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_all_unread_messages(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def delete_message(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)