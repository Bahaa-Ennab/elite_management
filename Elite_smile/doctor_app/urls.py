from django.urls import path
from . import views

urlpatterns = [
# path('', views.home, name='doctor_home'),
path('add_patient', views.add_patient, name='add_patient'),
path('working_hours', views.working_hours, name='working_hours'),
path('book_appointment', views.book_appointment, name='book_appointment'),
path('all_patients', views.all_patients, name='all_patients_display'),
path('appointments/<int:id>/edit/', views.edit_appointment, name='edit_appointment'),
path('appointments/<int:id>/delete/', views.delete_appointment, name='delete_appointment'),
path('admin_main_page', views.admin_main_page, name='admin_main_page'),
path('log_out', views.log_out, name='log_out'),
path('edit_user_info', views.edit_user_info, name='edit_user_info'),
path('patient_details_display/<int:patientid>', views.patient_details_display, name='patient_details_display'),
path('delete_patient/<int:patientid>', views.delete_patient, name='delete_patient'),
path('edit_patient_display/<int:patientid>', views.edit_patient_display, name='edit_patient_display'),
path('update_user_info/<int:patientid>', views.update_user_info, name='update_user_info'),
path('doctor/get_user_info/', views.get_user_info, name='get_user_info'),
path('add_user_display/', views.add_user_display, name='add_user_display'),
path('add_users_role', views.add_users_role, name='add_users_role'),
path('all_users', views.all_users, name='all_users'),
path('book_appointment_post', views.book_appointment_post, name='book_appointment_post'),
path('filter_appointments', views.filter_appointments, name='filter_appointments'),
]
