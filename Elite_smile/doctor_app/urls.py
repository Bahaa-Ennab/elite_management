from django.urls import path
from . import views

urlpatterns = [
# path('', views.home, name='doctor_home'),
path('add_patient', views.add_patient, name='add_patient'),
path('working_hours', views.working_hours, name='working_hours'),
path('book_appointment,', views.book_appointment, name='book_appointment'),
path('all_patients', views.all_patients, name='all_patients_display'),
path('appointments/<int:id>/edit/', views.edit_appointment, name='edit_appointment'),
path('appointments/<int:id>/delete/', views.delete_appointment, name='delete_appointment'),
path('admin_main_page', views.admin_main_page, name='admin_main_page'),
path('log_out', views.log_out, name='log_out'),
]