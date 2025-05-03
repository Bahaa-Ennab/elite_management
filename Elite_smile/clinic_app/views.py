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

def send_inquiry(request):
    models.Message.send_inquiry(request)
    return redirect('/contact')


def signup_in(request):
    return render(request, 'clinic/signup_in.html')

def register(request):
    if request.method == 'POST':
        errors = models.User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            request.session['register_errors'] = errors
            request.session['register_data'] = {
                'first_name': request.POST.get('first_name', ''),
                'last_name': request.POST.get('last_name', ''),
                'email': request.POST.get('email', ''),
                'confirm_email': request.POST.get('confirm_email', ''),
            }
            return redirect('/signup_in')
        else:
            models.User.register(request.POST)
            messages.success(request, "تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول.")
            request.session.pop('register_errors', None)
            request.session.pop('register_data', None)
            return redirect('/signup_in')
    return redirect('/signup_in')

def sign_in(request):
    if request.method == 'POST':
        email = models.User.objects.filter(email=request.POST['email'])
        if email:
            logged_user = email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                user=models.User.get_user(request)
                if user.role == 'patient':
                    return redirect('patient/patient_home_display')
                else:
                    return redirect('doctor/admin_main_page')

            else:
                messages.error(request, "كلمة المرور غير صحيحة")
        else:
            messages.error(request, "البريد الالكتروني غير مسجل")
    
    return redirect('/signup_in')  


