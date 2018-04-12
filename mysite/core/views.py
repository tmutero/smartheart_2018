from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from datetime import datetime, date
from mysite.core.forms import SignUpForm
from .models import *


@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def create_patient(request):


    patient = Patient(firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                       contact=request.POST['contact'],address=request.POST['address'],
                      gender=request.POST['gender'])

    patient.save()
    return redirect('read_patient')


def read_patient(request):
    patients = Patient.objects.all()
    print("=========================")
    print(patients)
    context = {'patients': patients}
    return render(request, 'patient/list.html', context)


def edit_patient(request, id):
    patient = Patient.objects.get(id=id)
    context = {'patient': patient}
    return render(request, 'patient/edit.html', context)


def update_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient.firstname = request.POST['firstname']
    patient.lastname = request.POST['lastname']
    patient.save()
    return redirect('/read_patient/')

def view_patient_record(request, id):
    print("-------------------------",id)
    patient=Patient.objects.get(id=id)
    patient_record=PatientRecords.objects.filter(patient_id=id)
    print("============================================================")
    print(patient_record)

    contex={'patient':patient,
            'patient_record':patient_record}
    return render(request,'patient/view.html',contex)

