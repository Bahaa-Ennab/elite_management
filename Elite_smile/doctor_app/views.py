from django.shortcuts import render,redirect
from . import models
from clinic_app.models import User


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
            
            # Filter patients (not role='role', but role='patient')

            return render(request, 'doctor/book_appointment.html')
        else:
            return redirect('/sign_in')  # or return an error page



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
    # هنا يمكنك إضافة منطق لجلب بيانات المرضى أو المواعيد من قاعدة البيانات
    return render(request, 'doctor/admin_main_page.html')

def edit_user_info(request):
    User.edit_user_info(request)
    return redirect('/doctor/add_patient')

def patient_details_display(request,patientid):
    context={
        'patient':User.objects.get(id=patientid)
    }
    return render(request,'doctor/patient_details_display.html',context)

def log_out(request):
    request.session.flush()
    return redirect('/')