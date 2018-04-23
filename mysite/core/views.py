from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from datetime import datetime, date
from mysite.core.forms import SignUpForm
from .models import *
from xhtml2pdf import pisa
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import time
import pandas as pd
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
                      gender=request.POST['gender'],birth_date=request.POST['birth_date'])

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

def create_patient_clinical(request):
    patient_id=request.POST.get('patient_id')
    print("==========================",patient_id)

    patient_record=PatientRecords(chest_pain = request.POST['chest_pain'],trestbps = request.POST['chest_pain'],
    chol =request.POST['chol'],
    fbs = request.POST['fbs'],
    restEcg =request.POST['restEcg'],
    thalach = request.POST['thalach'],
    exang = request.POST['exang'],
    oldPeak =request.POST['oldPeak'],
    slope = request.POST['slope'],
    ca = request.POST['ca'],
    thal = request.POST['thal'],
    patient_id=patient_id)
    print("========================================================",patient_record)
    patient_record.save()


    return redirect('view_patient_record',patient_id)

def read_user(request):
    users = User.objects.all()

    print(users)
    context = {'users': users}
    return render(request, 'user/list.html', context)

def create_drug(request):


    drug = Drug(name=request.POST['name'], type=request.POST['type'],
                formulation=request.POST['formulation'])
    drug.save()
    return redirect('read_drug')

def read_drug(request):
    drugs = Drug.objects.all()

    print(drugs)
    context = {'drugs': drugs}
    return render(request, 'drug/list.html', context)



#process

def process(request,  precord_id,id):

    patient = Patient.objects.get(id=id)
    patient_record1 = PatientRecords.objects.get(id=precord_id)

    print("--------------------------------Record Value------------------------------------------------------------",
          precord_id)
    print("-=========================================--Patient----------------------------------------", id)
    data = pd.read_csv("uploads/final.csv")


    data = data[[
        "pregnant",
        "glucose",
        "pressure",
        "skin",
        "insulin",
        "mass",
        "pedegree",
        "age",
        "class"

    ]].dropna(axis=0, how='any')


    X_train, X_test = train_test_split(data, test_size=0.5, random_state=int(time.time()))
    gnb = GaussianNB()
    used_features = [
        "pregnant",
        "glucose",
        "pressure",
        "skin",
        "insulin",
        "mass",
        "pedegree",
        "age",

    ]
    gnb.fit(
        X_train[used_features].values,
        X_train["class"]
    )


    return