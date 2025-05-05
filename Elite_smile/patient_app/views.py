from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
import bcrypt
from clinic_app.models import Appointment,AppointmentManager,User

# Create your views here.
def patient_home_display(request):
    userid=request.session['userid']
    user=models.User.objects.get(id=userid)
    context={
        'user':models.User.get_user(request),
        'patient': models.User.get_user(request),
        'doctors':models.User.objects.filter(role="doctor")

    }
    return render(request,'patient_home_page.html',context)

def log_out(request):
    user=models.User.get_user(request)
    request.session.flush()
    return redirect('/')

def book_appointment_display(request):
    context={
        'doctors':models.User.objects.filter(role="doctor")
    }
    return render(request,'book_appointment_display.html',context)

def book_appointment(request):
    if request.method == "POST":
        postData = request.POST.copy()
        postData['doctor_id'] = request.POST['doctor_id']  # نضيف doctor_id مؤقتًا لتمريره للـ validator

        errors = Appointment.objects.appointment_validator(postData)

        if errors:
            context = {
            'doctors': User.objects.filter(role='doctor'),
            'error_messages':errors
            
            }
            return render(request, 'book_appointment_display.html',context)
        Appointment.book_appointment_post_for_patient(request)
        return redirect('/patient/patient_home_display')        
    return redirect('/patient/patient_home_display')        


