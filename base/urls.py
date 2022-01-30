from django.urls import path
from . import views




urlpatterns = [
    path('login', views.LoginPage, name="LoginPage"),
    path('logout', views.LogOutPage, name="LogOutPage"),
    path('register', views.registerPage, name="register"),
    
    path('', views.home, name="home"),
    path('room/<str:id>/', views.room, name="room"),
    path('profile/<str:id>/', views.profile, name="profile"),
    path('create-room', views.createRoom, name="createRoom"),
    path('update-room/<str:id>/', views.updateRoom, name="updateRoom"),
    path('remove-room/<str:id>/', views.removeRoom, name="removeRoom"),
    path('delete-Msg/<str:id>/', views.deleteMsg, name="deleteMsg"),
    path('update-user/', views.UpdateUser, name="UpdateUser"),
    path('topics/', views.TopicPage, name="TopicPage"),
    path('activity/', views.ActivityPage, name="ActivityPage")
   


]
