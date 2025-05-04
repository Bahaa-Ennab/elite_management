from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
import bcrypt
from django.conf import settings
from django.http import JsonResponse
from .models import Appointment, User
from datetime import datetime, timedelta
import openai
from django.conf import settings

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
    context = {
        'register_errors': request.session.get('register_errors'),
        'register_data': request.session.get('register_data'),
    }
    # بعد ما نحضّر البيانات للعرض، نمسحها من الجلسة
    request.session.pop('register_errors', None)
    request.session.pop('register_data', None)
    return render(request, 'clinic/signup_in.html', context)

def signup_in(request):
    context = {
        'register_errors': request.session.get('register_errors'),
        'register_data': request.session.get('register_data'),
    }
    # بعد ما نحضّر البيانات للعرض، نمسحها من الجلسة
    request.session.pop('register_errors', None)
    request.session.pop('register_data', None)
    return render(request, 'clinic/signup_in.html', context)

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

openai.api_key = settings.OPENAI_API_KEY

# إنشاء دالة لإرسال المحادثة إلى API
def chat_with_gpt(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')  # مدخل المستخدم من الفورم

        try:
            openai.api_key = settings.OPENAI_API_KEY
            # إرسال الطلب إلى API و استلام الرد
            response = openai.ChatCompletion.create(
                model="gpt-4.1",  # أو "gpt-4" إذا كنت تستخدمه
        messages=[
        {
            "role": "system",
            "content": "أنت مساعد ذكي تعمل في عيادة أسنان اسمك وسيم، وتتحدث باسم الدكتور وسيم. يجب أن تكون ردودك احترافية، طبية، وتظهر التعاطف، وتركّز فقط على صحة الأسنان والفم والمواعيد. إذا سُئلت عن شيء خارج هذا النطاق، اعتذر بلُطف وأعد توجيه المستخدم."

        },
        {
            "role": "assistant",
            "content": "مرحباً، معك الدكتور وسيم من عيادة إيليت سمايل، كيف يمكنني مساعدتك؟"
        },
        {
            "role": "user",
            "content": user_input
        }
    ],
                max_tokens=150,
                temperature=0.7  # التحكم في درجة العشوائية في الرد
            )

            # استرجاع الرد
            gpt_response = response['choices'][0]['message']['content'].strip()
            return JsonResponse({'response': gpt_response})
        
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'clinic/chat_interface.html')