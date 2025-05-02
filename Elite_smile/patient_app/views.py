from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
import bcrypt
# Create your views here.
def patient_home_display(request):
    context={
        'user':models.User.get_user(request)
    }
    return render(request,'patient_home_page.html',context)

def log_out(request):
    user=models.User.get_user(request)
    request.session.flush()
    return redirect('/')