from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from base import views

urlpatterns = [
    path('login',views.loginage,name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),

    path('userProfile/<int:pk>', views.userProfile, name='userProfile'),

    path('',views.home,name='home'),
    path('room/<int:pk>',views.room,name='room'),
    path('createRoom',views.createRoom,name='createRoom'),
    path('updateRoom/<int:pk>', views.updateRoom, name='updateRoom'),
    path('deleteRoom/<int:pk>', views.deleteRoom, name='deleteRoom'),
    path('deleteMessage/<int:pk>', views.deleteMessage, name='deleteMessage'),

    path('updateUser', views.updateUser, name='updateUser'),
    path('topicPage', views.topicPage, name='topicPage'),
    path('activityPage', views.activityPage, name='activityPage'),

    path('change_password',views.change_password,name='change_password'),

    path('reset_password',auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_send', auth_views.PasswordResetDoneView.as_view(),name= "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),name ="password_reset_complete"),

]
