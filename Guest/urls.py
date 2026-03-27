from django.urls import path
from Guest import views

app_name="Guest"

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('verify/', views.face_verify, name='face_verify'),
    path('live/', views.live_face, name='live_face'),
]