from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from academic.models import Bulletin


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


from academic.models import Message
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from academic.serializers import MessageSerializer


@api_view(['GET', 'POST'])
def message_list(request):
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