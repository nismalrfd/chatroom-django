from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from base.models import Room
from .forms import *


def loginage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            print(request.user)
        else:
            messages.error(request, 'user does not exist')

    context = {'page': page}
    return render(request, 'login_register.html', context)




def registerUser(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.warning(request, 'username already exists')
                return redirect('/register')
            if confirm_password and password and password != confirm_password:
                messages.warning(request, 'password not matching !')
                return redirect('/register')

            user_obj = User.objects.create(username=username)

            user_obj.set_password(password)
            user_obj.save()

            messages.success(request, 'Account created')
            return redirect('login')
        except Exception as e:
            messages.warning(request, 'Something went wrong')

    return render(request, 'login_register.html')
def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topic = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topic': topic, 'room_count': room_count
        , 'room_messages': room_messages}
    return render(request, 'home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topic = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages,
               'topic': topic}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topic = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created =Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host =request.user,
            topic =topic,
            name =request.POST.get('name'),
            description = request.POST.get('description')

        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')

    context = {'form': form,'topic':topic}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topic = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("you are not allowes here !!")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)
        room.name =request.POST.get('name')
        room.topic =topic
        room.description =request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form,'topic':topic,"room":room}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("you are not allowes here !!")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("you are not allowed here !!")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user =request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile',pk=user.id)
    context ={'form':form}
    return render(request,'edit-user.html',context)

def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topic = Topic.objects.filter(name__contains=q)
    return render(request,'topics.html',{'topic':topic})
def activityPage(request):
    room_messages =Message.objects.all()
    return render(request,'activity.html',{'room_messages':room_messages})


def changePassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            if not user.check_password(current_password):
                messages.warning(request, "your old password is not correct!")
            else:
                if new_password != confirm_password:
                    messages.warning(request, "your new password not match the confirm password !")

                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "your password has been changed successfuly.!")
                    return redirect('/')

    return render(request, 'password_change.html')