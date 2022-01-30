
from calendar import c
import imp
from pydoc_data.topics import topics
import re
from telnetlib import AUTHENTICATION
from django.forms import forms
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import context
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Message, Room, Topic
from .forms import RoomForm, UserForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

# rooms =[
#     {'id': 1, 'name': 'lets talk shit'},
#     {'id': 2, 'name': 'lets talk Science'},
#     {'id': 3, 'name': 'lets talk Football'},
#     {'id': 4, 'name': 'lets talk Python '},


# ]


def LoginPage(request):

    page = 'loginPage'
    if request.user.is_authenticated:
        return redirect('home')



    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request,'Username or password incorrect')
                

    context = {'page': page}
    return render(request, 'base/login-register.html', context)


def LogOutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            #login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Errrrr' )
    return render(request, 'base/login-register.html', {'form':form})



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
         Q(topic__name__icontains=q) |
         Q(host__username__icontains=q) |
         Q(name__icontains=q) 
        )     
    
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    coms = Message.objects.filter(
        Q(room__topic__name__icontains=q) 
        

    ) 



    return render(request, 'base/home.html' , {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'coms':coms} )

def room(request, id):
    room = Room.objects.get(id=id)
    # for i in rooms:
    #     if i['id'] == int(id):
    #         room = i

    coms = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        msg = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )

        room.participants.add(request.user)
        return redirect('room', id= room.id)
       
    context = {'room': room , 'coms': coms,
     'participants': participants}        
    return render(request, 'base/room.html', context)    
 

def profile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    coms = user.message_set.all()
    topics = Topic.objects.all()



    context = {'user':user,'rooms':rooms, 'coms':coms, 'topics':topics}
    return render(request, 'base/profile.html', context)









@login_required(login_url='LoginPage') 
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name =topic_name)
        
        Room.objects.create(
            host = request.user,
            topic= topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )

        #form = RoomForm(request.POST)
        # if form.is_valid():
            # room = form.save(commit=False)
            # room.host = request.user
            # room.save()
        return redirect('home')

    context ={'form' : form, 'topics':topics}
    return render(request, 'base/room_form.html', context)
    

@login_required(login_url='LoginPage') 
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here BIT')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name =topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
       
        return redirect('home')
    context ={'form' : form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='LoginPage') 
def removeRoom(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('You are not allowed here BIT')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='LoginPage') 
def deleteMsg(request, id):
    message = Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse('You are not allowed here BIT')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='LoginPage') 
def UpdateUser(request):
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid:
            form.save()
            return redirect('profile', id=request.user.id)


    return render(request, 'base/Update-user.html', {'form':form})


def TopicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'base/topics_new.html',{'topics':topics})


def ActivityPage(request):
    coms =  Message.objects.all()
     

    return render(request, 'base/activity-new.html',{'coms':coms})
