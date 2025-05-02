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
    first_name= models.CharField(max_length=255)
    last_name=  models.CharField(max_length=255)
    email=  models.CharField(max_length=255)
    password=  models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def get_id(request):
        user=User.objects.filter(id=request.session['userid'])
        return user

    def register(post):
        first_name= post['first_name']
        last_name=  post['last_name']
        email=  post['email']
        password=post ['password']
        password_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password_hash)
