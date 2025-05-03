from django.db import models
from datetime import date
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 3:
            errors["first_name"] = "الاسم الاول يجب ان يتكون على الاقل من حرفين"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "اسم العائلة يجب ان يتكون على الاقل من حرفين"
        if len(postData['password']) < 9:
            errors["password"] = "كلمة المرور يجب ان تتكون من ثمانية حروف على الاقل"
        if postData['password'] != postData['confirm_password']:
            errors["password"] = "كلمة السر لا تتطابق مع التأكيد"
        if postData['email'] != postData['confirm_email']:
            errors["email"] = "يجب ان يكون البريد الالكتروني متطابق مع التأكيد"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "بريد الكتروني خاطئ"
        if self.model.objects.filter(email=postData['email']).exists():
            errors['email'] = "هذا البريد مسجل مسبقا"

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
        
