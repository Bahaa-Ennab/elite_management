from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
import bcrypt
from clinic_app.models import Appointment,AppointmentManager,User
from django.views.decorators.cache import never_cache


# Create your views here.
 
@never_cache
def patient_home_display(request):
    if 'userid' in request.session:
        userid=request.session['userid']
        user=models.User.objects.get(id=userid)
        appointments = Appointment.objects.filter(patient=user).order_by('start_at_date', 'start_at_time')
        context={
            'user':models.User.get_user(request),
            'patient':models.User.get_user(request),
            'doctors':models.User.objects.filter(role="doctor"),
            'appointments':appointments

        }
        return render(request,'patient_home_page.html',context)
    return redirect('/')

def log_out(request):
    if 'userid' in request.session:
        user=models.User.get_user(request)
        request.session.flush()
        return redirect('/')
    return redirect('/')

def book_appointment(request):
    if 'userid' in request.session:
        if request.method == "POST":
            postData = request.POST.copy()
            postData['doctor_id'] = request.POST['doctor_id']  # نضيف doctor_id مؤقتًا لتمريره للـ validator

            errors = Appointment.objects.appointment_validator(postData)

            if errors:
                context = {
                'doctors': User.objects.filter(role='doctor'),
                'error_messages':errors
                
                }
                return render(request, 'patient_home_page.html',context)
            Appointment.book_appointment_post_for_patient(request)
            return redirect('/patient/patient_home_display')        
        return redirect('/patient/patient_home_display')        
    return redirect('/')


