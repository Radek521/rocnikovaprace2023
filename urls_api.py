from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('mistnosti/', views.getRooms),
    path('mistnosti/<str:pk>/', views.getRoom),
]