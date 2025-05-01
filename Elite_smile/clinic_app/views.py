from django.shortcuts import render

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