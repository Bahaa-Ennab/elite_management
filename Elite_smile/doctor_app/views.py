from django.shortcuts import render,redirect
from . import models
from clinic_app.models import User
from clinic_app.models import Appointment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.

def add_patient(request):
    user_id = request.session['userid']
    context = {
            'patients': User.objects.filter(role='patient')
        }

    return render(request, 'doctor/add_patient.html',context)

def working_hours(request):
    days = ['السبت', 'الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة']

    if request.method == 'POST':
        active_days = request.POST.getlist('active_days')
        working_hours = {}

        for day in days:
            if day in active_days:
                from_time = request.POST.get(f'from_{day}')
                to_time = request.POST.get(f'to_{day}')
                working_hours[day] = {'from': from_time, 'to': to_time}

        print(working_hours)  # فقط للفحص
        return redirect('/admin_main_page')  # أو أي صفحة نجاح بعد الحفظ

    # في حالة GET (أول ما يفتح الصفحة)
    return render(request, 'doctor/working_hours.html', {'days': days})

def book_appointment(request):
        if 'userid' in request.session:
            # Get the user ID from the session
            context = {
            'patients': User.objects.filter(role='patient')
        }

            
            # Filter patients (not role='role', but role='patient')

            return render(request, 'doctor/book_appointment.html',context)
        else:
            return redirect('/sign_in')  # or return an error page
        
def book_appointment_post(request):
    Appointment.book_appointment_post(request)
    return redirect('/doctor/book_appointment')


def filter_appointments(request):
    context={
        'appointments':Appointment.filter_appointments(request)
    }
    return render(request, 'doctor/admin_main_page.html',context)


def all_patients(request):
    context = {
            'patients': User.objects.filter(role='patient')
        }
    return render(request, 'doctor/all_patients_display.html', context)

def edit_appointment(request, id):
    # appointment = get_object_or_404(Appointment, id=id)
    # هنا من الأفضل تستخدم ModelForm للمواعيد
    if request.method == 'POST':
        # معالجة النموذج وتحديث الموعد
        ...
    # return render(request, 'doctor/edit_appointment.html', {'appointment': appointment})
    return render(request, 'doctor/edit_appointment.html')


def delete_appointment(request, id):
    # appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        # appointment.delete()
        return redirect('admin_main_page')
    
def admin_main_page(request):
    context={
        'appointments':Appointment.get_appointments(),
    }
    # هنا يمكنك إضافة منطق لجلب بيانات المرضى أو المواعيد من قاعدة البيانات
    return render(request, 'doctor/admin_main_page.html',context)

def edit_user_info(request):
    User.edit_user_info(request)
    return redirect('/doctor/add_patient')

def patient_details_display(request,patientid):
    context={
        'patient':User.objects.get(id=patientid)
    }
    return render(request,'doctor/patient_details_display.html',context)

def delete_patient(request,patientid):
    patient=User.objects.get(id=patientid)
    patient.delete()
    if patient.role == 'patient':
        return redirect('/doctor/all_patients')
    else:
        return redirect('/doctor/all_users')



def edit_patient_display(request,patientid):
    context={
        'patient':User.objects.get(id=patientid)
    }
    return render(request,'doctor/edit_patient_display.html',context)

def update_user_info(request,patientid):
    User.update_user_info(request,patientid)
    return redirect(f'/doctor/patient_details_display/{patientid}')


def get_user_info(request):
    user_id = request.GET.get('user_id')
    print("Received user_id:", user_id)

    if user_id:
        try:
            user = User.objects.get(id=user_id)
            user_info = {
                'email': user.email,
                'phone': user.phone,
                'role': user.role,
            }
            return JsonResponse(user_info)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid user ID'}, status=400)

def add_user_display(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'doctor/add_user_display.html', context)

def add_users_role(request):
    User.add_users_role(request)
    return redirect('/doctor/all_users')

def all_users(request):
    context={
        'users':User.users_not_patient(request)
    }
    return render(request,'doctor/all_users.html',context)


def log_out(request):
    request.session.flush()
    return redirect('/')