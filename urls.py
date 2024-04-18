#url file pro specifickou aplikaci

from django.urls import path
from .import views

#zde volame cesty z views.py
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.domovska, name='domovska'),
    #do urls muzeme davat dynamickou hodnotu
     path('mistnost/<str:pk>/', views.mistnost, name='mistnost'),
     path('profil/<str:pk>/', views.userProfil, name='user-profil'),

     path('vytvor-mistnost', views.vytvorMistnost, name='vytvor-mistnost'),
     path('uprav-mistnost/<str:pk>/', views.upravMistnost, name='uprav-mistnost'),
     path('delete-mistnost/<str:pk>/', views.deleteMistnost, name='delete-mistnost'),
     path('delete-zprava/<str:pk>/', views.deleteZprava, name='delete-zprava'),
     path('update-user/', views.updateUser, name='update-user')
]    