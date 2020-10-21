from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from academic.models import Bulletin
from datetime import datetime
from academic.models import Message, User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from academic.serializers import MessageSerializer
import uuid


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
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if username == "":
            return HttpResponse("No username!")
        if password == "":
            return HttpResponse("No password!")
        if email == "":
            return HttpResponse("No email!")
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


@api_view(['GET'])
def message_list(request):
    """
    this function returns all messages from db
    """
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def write_message(request):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        if request.method == 'POST':
            serializer = MessageSerializer(data=request.data)
            message = Message()
            message.id = uuid.uuid4().int
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
    except Exception as e:
        pass
    finally:
        return Response("Wrong body for write_message POST request",
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def all_messages_for_user(request):
    """
    this function receives a user and returns all the messages for the user.
    if user doesn't exist , the response will be no data for user.
    """
    try:
        if request.method == 'POST':
            expected_user = request.data['user']
            users = User.objects.all()
            for user in users:
                if expected_user == user.get_username():
                    messages_for_user = Message.objects.filter(receiver=user.get_username())
                    serializer = MessageSerializer(messages_for_user, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("No data for user {}".format(request.data['user']),
                            status=status.HTTP_200_OK)
    except Exception as e:
        pass
    finally:
        return Response("unable to get all messages for user {}".format(request.data['user']),
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def read_message(request):
    """
    read message for a given user and id
    """
    try:
        if request.method == 'POST':
            expected_user = request.data['user']
            expected_id = request.data['id']
            users = User.objects.all()
            for user in users:
                if expected_user == user.get_username():
                    messages = Message.objects.filter(receiver=user.get_username())
                    message_by_id = messages.get(id=expected_id)
                    message_by_id.read_by_receiver = True
                    message_by_id.save()
                    serializer = MessageSerializer(message_by_id, many=True)
                    return Response(serializer.data)
            return HttpResponse("No data for user {}".format(request.data))
    except Exception as e:
        pass
    finally:
        return Response("unable to read message for user {} and id {}".
                        format(request.data['user'], request.data['id']), status=status.HTTP_200_OK)




@api_view(['POST'])
def get_all_unread_messages_for_user(request):
    """
    List all code snippets, or create a new snippet.
    """
    expected_user = ''
    try:
        if request.method == 'POST':
            expected_user = request.data['user']
            users = User.objects.all()
            for user in users:
                if expected_user == user.get_username():
                    messages = Message.objects.filter(receiver=user.get_username(), read_by_receiver=False)
                    serializer = MessageSerializer(messages, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return HttpResponse("No data for user {}".format(request.data))
    except Exception as e:
        pass
    finally:
        return HttpResponse("Unable to get all unread messages for user {}".format(expected_user),
                            status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def delete_message(request):
    """
    upon receiving user name and id from request, this function
    deletes the message for user if exists
    """
    expected_user = ''
    expected_id = ''
    try:
        expected_user = request.data['user']
        expected_id = request.data['id']
        if request.method == 'POST':
            users = User.objects.all()
            for user in users:
                if expected_user == user.get_username():
                    messages = Message.objects.filter(receiver=user.get_username())
                    message_by_id = messages.get(id=expected_id)
                    message_by_id.delete()
                    serializer = MessageSerializer(messages, many=True)
                    return Response(serializer.data)
            if expected_user == 'root':
                messages = Message.objects.all()
                message_by_id = messages.get(id=expected_id)
                message_by_id.delete()
                serializer = MessageSerializer(message_by_id, many=True)
                return Response(serializer.data)
    except Exception as e:
        pass
    finally:
        return HttpResponse("Unable to delete a message with id {}".format(expected_id),
                            status=status.HTTP_400_BAD_REQUEST)
