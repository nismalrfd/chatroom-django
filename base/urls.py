from django.contrib import admin
from django.urls import path, include

from base import views

urlpatterns = [
    path('login',views.loginage,name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),

    path('userProfile/<int:pk>', views.userProfile, name='userProfile'),
    path('changePassword', views.changePassword, name='changePassword'),

    path('',views.home,name='home'),
    path('room/<int:pk>',views.room,name='room'),
    path('createRoom',views.createRoom,name='createRoom'),
    path('updateRoom/<int:pk>', views.updateRoom, name='updateRoom'),
    path('deleteRoom/<int:pk>', views.deleteRoom, name='deleteRoom'),
    path('deleteMessage/<int:pk>', views.deleteMessage, name='deleteMessage'),

    path('updateUser', views.updateUser, name='updateUser'),
    path('topicPage', views.topicPage, name='topicPage'),
    path('activityPage', views.activityPage, name='activityPage')

]
