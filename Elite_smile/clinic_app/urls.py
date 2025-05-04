from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('doctors/', views.doctors, name='doctors'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('signup_in/', views.signup_in, name='signup_in'),
    path('register', views.register, name='register'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('send_inquiry', views.send_inquiry, name='send_inquiry'),
    path('chat/', views.chat_with_gpt, name='chat_with_gpt')
    # 
]   