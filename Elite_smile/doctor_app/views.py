from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
import bcrypt

# Create your views here.

def add_patient(request):
    if request.method == 'POST':
        # Process the form data and save the patient information
        pass  # Replace with your logic to handle form submission
    return render(request, 'doctor/add_patient.html')

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
    if request.method == 'POST':
        # Process the form data and save the appointment information
        pass  # Replace with your logic to handle form submission
    return render(request, 'doctor/book_appointment.html')

def all_patients(request):
    # هنا يمكنك إضافة منطق لجلب بيانات المرضى من قاعدة البيانات
    patients = []  # استبدل هذا بقائمة المرضى الفعلية
    return render(request, 'doctor/all_patients_display.html', {'patients': patients})

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

def log_out(request):
    request.session.flush()
    return redirect('/')