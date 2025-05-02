from django.urls import path
from . import views

urlpatterns = [
    path('patient_home_display', views.patient_home_display, name='patient_home'),
    path('log_out', views.log_out, name='log_out'),

]
