from django.db import models
from datetime import date
import re
import bcrypt
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        required_fields = ['first_name', 'last_name', 'email', 'confirm_email', 'password', 'confirm_password']
        for field in required_fields:
            if not postData.get(field):
                errors[field] = "هذا الحقل مطلوب"
        if len(postData['first_name']) < 3:
            errors["first_name"] = "الاسم الأول يجب ان يتكون على الاقل من 3 حروف"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "اسم العائلة يجب ان يتكون على الاقل من 3 حروف"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "البريد الكتروني غير صالح"
        elif postData['email'] != postData['confirm_email']:
            errors["email"] = "يجب أن يكون البريد الالكتروني متطابقاً مع التأكيد"
        elif self.model.objects.filter(email=postData['email']).exists():
            errors["email"] = "هذا البريد مسجل مسبقًا"
        if len(postData['password']) < 9:
            errors["password"] = "كلمة السر يجب أن تكون 9 أحرف على الأقل"
        elif postData['password'] != postData['confirm_password']:
            errors["password"] = "كلمة السر غير متطابقة  "
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255, default='patient')
    doctor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='patients')
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)  # No need for null=True in CharField
    social_status = models.CharField(max_length=20, blank=True)
    id_number = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    chronic_disease = models.BooleanField(default=False)
    takes_medications = models.BooleanField(default=False)
    drug_allergy = models.BooleanField(default=False)
    allergy_details = models.TextField(blank=True)
    dialysis =models.BooleanField(default=False)
    treatment_plan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


    def get_user(request):
        user=User.objects.get(id=request.session['userid'])
        return user
    
    def get_patient():
        patient=User.objects.filter(role=patient)
        return patient
    
    def register(post):
        first_name= post['first_name']
        last_name=  post['last_name']
        email=  post['email']
        password=post ['password']
        password_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        role=post['role']

        User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password_hash,role=role)

    def edit_user_info(request):
        patient_id = request.POST.get('patient_id')  # اسم الحقل في الفورم هو pateints_names
        patient = User.objects.get(id=patient_id)

        # بيانات موجودة مسبقًا في patient
        first_name = patient.first_name
        last_name = patient.last_name
        email = patient.email
        password = patient.password
        role = patient.role

        doctor_id = request.session['userid']
        doctor = User.objects.get(id=doctor_id)

        # بيانات مأخوذة من الفورم
        birth_date = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        id_number = request.POST.get('id_number')
        phone = request.POST.get('phone')
        chronic_disease = request.POST.get('chronic_disease', 'no')
        current_medication = request.POST.get('current_medication', 'no')
        drug_allergy = request.POST.get('drug_allergy', 'no')
        allergy_details = request.POST.get('allergy_details', '')
        dialysis = request.POST.get('dialysis', 'no')
        dialysis_details = request.POST.get('dialysis_details', '')

        # تحديث بيانات المريض
        patient.first_name = first_name
        patient.last_name = last_name
        patient.email = email
        patient.password = password
        patient.role = role
        patient.doctor = doctor
        patient.birth_date = birth_date
        patient.gender = gender
        patient.social_status = marital_status
        patient.id_number = id_number
        patient.phone = phone
        patient.chronic_disease = chronic_disease
        patient.takes_medications = current_medication
        patient.drug_allergy = drug_allergy
        patient.allergy_details = allergy_details
        patient.dialysis = dialysis
        patient.treatment_plan = dialysis_details

        patient.save()

    def update_user_info(request,patientid):
        patient = User.objects.get(id=patientid)

        # بيانات موجودة مسبقًا في patient
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        role = patient.role

        doctor_id = request.session['userid']
        doctor = User.objects.get(id=doctor_id)

        # بيانات مأخوذة من الفورم
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        id_number = request.POST.get('id_number')
        phone = request.POST.get('phone')
        chronic_disease = request.POST.get('chronic_disease')
        current_medication = request.POST.get('current_medication') == 'True'
        drug_allergy = request.POST.get('drug_allergy')
        allergy_details = request.POST.get('allergy_details')
        dialysis = request.POST.get('dialysis')
        dialysis_details = request.POST.get('dialysis_details')

        # تحديث بيانات المريض
        patient.first_name = first_name
        patient.last_name = last_name
        patient.email = email
        patient.password = password_hash
        patient.role = role
        patient.doctor = doctor
        patient.birth_date = birth_date
        patient.gender = gender
        patient.social_status = marital_status
        patient.id_number = id_number
        patient.phone = phone
        patient.chronic_disease = chronic_disease
        patient.takes_medications = current_medication
        patient.drug_allergy = drug_allergy
        patient.allergy_details = allergy_details
        patient.dialysis = dialysis
        patient.treatment_plan = dialysis_details

        patient.save()

    def users_not_patient(request):
        return User.objects.exclude(role='patient')
    
    def add_users_role(request):
        user=User.objects.get(id=request.POST.get('user_id'))
        first_name=user.first_name
        last_name=user.last_name
        email=request.POST['email']
        phone=request.POST['phone']
        role=request.POST['role']

        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.phone=phone
        user.role=role

        user.save()
        

class Message(models.Model):
        name=models.CharField(max_length=255)
        email=models.CharField(max_length=255)
        message=models.TextField()
        created_at= models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        
        def send_inquiry(request):
            name =request.POST['name']
            email =request.POST['email']
            message =request.POST['message']
            Message.objects.create(name=name,email=email,message=message)


from django.utils import timezone
from datetime import datetime, timedelta

class AppointmentManager(models.Manager):
    def appointment_validator(self, postData):
        errors = {}

        required_fields = ['patient_id', 'start_at']
        for field in required_fields:
            if not postData.get(field):
                errors[field] = "هذا الحقل مطلوب"

        try:
            start_at = datetime.strptime(postData['start_at'], "%Y-%m-%dT%H:%M")
            start_at = timezone.make_aware(start_at)
            end_at = start_at + timedelta(minutes=30)
        except (ValueError, KeyError):
            errors['start_at'] = "صيغة التاريخ غير صحيحة"
            return errors

        if start_at < timezone.now():
            errors['start_at'] = "لا يمكن تحديد موعد في الماضي"

        doctor_id = postData.get('doctor_id')
        if doctor_id:
            # نتحقق من وجود أي تقاطع في المواعيد
            overlapping_appointments = self.model.objects.filter(
                doctor_id=doctor_id,
                start_at_date__lt=end_at,
                end_at__gt=start_at
            )
            if overlapping_appointments.exists():
                errors['start_at'] = "يوجد موعد آخر لهذا الطبيب يتقاطع مع هذا التوقيت"

        return errors


class Appointment(models.Model):
    doctor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='doctor_appointments',limit_choices_to={'role': 'doctor'})
    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='patient_appointments',limit_choices_to={'role': 'patient'})
    start_at_date = models.DateTimeField()
    end_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    the_service = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()


    def filter_appointments(request):
        start_date_str=request.POST['start_date']
        end_date_str=request.POST['end_date']
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        filtered_appointments = Appointment.objects.filter(start_at_date__range=(start_date, end_date))
        end_date = end_date.replace(hour=23, minute=59, second=59)
        return filtered_appointments



    def get_appointments():
        return Appointment.objects.all()

    def book_appointment_post(request):
        doctor_id = request.session['userid']
        doctor = User.objects.get(id=doctor_id)
        patient_id=request.POST['patient_id']
        patient=User.objects.get(id=patient_id)
        start_at_raw=request.POST['start_at']
        start_at_date = datetime.strptime(start_at_raw, "%Y-%m-%dT%H:%M")
        end_at=start_at_date + timedelta(minutes=30)
        notes=request.POST['notes']
        the_service=request.POST['the_service']
        
        Appointment.objects.create(doctor=doctor,patient=patient,start_at_date=start_at_date,end_at=end_at,notes=notes,the_service=the_service)


