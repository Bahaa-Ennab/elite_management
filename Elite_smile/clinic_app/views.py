from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
import bcrypt

# Create your views here.
def home(request):
    return render(request, 'clinic/home.html')

def about(request):
    return render(request, 'clinic/about.html')

def doctors(request):
    return render(request, 'clinic/doctors.html')

def services(request):
    return render(request, 'clinic/services.html')

def contact(request):
    return render(request, 'clinic/contact.html')

def signup_in(request):
    return render(request, 'clinic/signup_in.html')

def register(request):
    if request.method == 'POST':
        errors = models.User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value) 
            return redirect('/signup_in')
        else:
            models.User.register(request.POST)
            messages.success(request, "تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول.")
            return redirect('/signup_in')
    return redirect('/signup_in')

def sign_in(request):
    if request.method == 'POST':
        email = models.User.objects.filter(email=request.POST['email'])
        if email:
            logged_user = email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('patient/patient_home_display')
            else:
                messages.error(request, "كلمة المرور غير صحيحة")
        else:
            messages.error(request, "البريد الالكتروني غير مسجل")
    
    return redirect('/signup_in')  


