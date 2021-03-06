from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Q, Count
import time
import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, date
import json
from django.template import loader

from mysite.core.forms import SignUpForm
from .models import *
from xhtml2pdf import pisa
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import time
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from twilio.rest import Client
from .credentials import ACCOUNT_SID,MY_CELL,MY_TWILO,AUTH_TOKEN

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
    if not request.user.is_authenticated:
        return redirect('home')

    patient = Patient(firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                       contact=request.POST['contact'],address=request.POST['address'],
                      gender=request.POST['gender'],birth_date=request.POST['birth_date'])

    patient.save()
    return redirect('read_patient')


def read_patient(request):
    if not request.user.is_authenticated:
        return redirect('home')
    patients = Patient.objects.all()

    print(patients)
    context = {'patients': patients}
    return render(request, 'patient/list.html', context)


def edit_patient(request, id):
    if not request.user.is_authenticated:
        return redirect('home')
    patient = Patient.objects.get(id=id)
    context = {'patient': patient}
    return render(request, 'patient/edit.html', context)


def update_patient(request, id):
    if not request.user.is_authenticated:
        return redirect('home')
    patient = Patient.objects.get(id=id)
    patient.firstname = request.POST['firstname']
    patient.lastname = request.POST['lastname']
    patient.save()
    return redirect('/read_patient/')

def view_patient_record(request, id):
    if not request.user.is_authenticated:
        return redirect('home')
    print("-------------------------",id)
    patient=Patient.objects.get(id=id)
    patient_record=PatientRecords.objects.filter(patient_id=id)
    print("============================================================")
    print(patient_record)

    contex={'patient':patient,
            'patient_record':patient_record}
    return render(request,'patient/view.html',contex)

def create_patient_clinical(request):
    if not request.user.is_authenticated:
        return redirect('home')
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

    patient_record.save()


    return redirect('view_patient_record',patient_id)

def read_user(request):
    if not request.user.is_authenticated:
        return redirect('home')
    users = User.objects.all()

    print(users)
    context = {'users': users}
    return render(request, 'user/list.html', context)

def create_drug(request):
    if not request.user.is_authenticated:
        return redirect('home')

    drug = Drug(name=request.POST['name'], type=request.POST['type'],
                formulation=request.POST['formulation'])
    drug.save()
    return redirect('read_drug')

def read_drug(request):
    if not request.user.is_authenticated:
        return redirect('home')
    drugs = Drug.objects.all()

    print(drugs)
    context = {'drugs': drugs}
    return render(request, 'drug/list.html', context)



#process

def process(request,  precord_id,id):
    if not request.user.is_authenticated:
        return redirect('home')

    patient = Patient.objects.get(id=id)
    patient_record1 = PatientRecords.objects.get(id=precord_id)

    print("--------------------------------Record Value------------------------------------------------------------",
          precord_id)
    print("-=========================================--Patient----------------------------------------", id)
    data = pd.read_csv("mysite/uploads/heart.csv")
    age=patient.age()
    sex=patient.gender
    chest_pain =patient_record1.chest_pain
    trestbps =patient_record1.trestbps
    chol =patient_record1.chol
    fbs =patient_record1.fbs
    restEcg =patient_record1.restEcg
    thalach =patient_record1.thalach
    exang =patient_record1.exang
    oldPeak =patient_record1.oldPeak
    slope =patient_record1.slope
    ca =patient_record1.ca
    thal =patient_record1.thal
    print("-------------------------------------")
    print("Age",age)
    print("Sex",sex)
    print("chest pain",chest_pain)
    print("trestbps",trestbps)
    print("Chol",chol)
    print("Fbs",fbs)
    print("Restecg",restEcg)
    print("Thalach",thalach)
    print("Exang",exang)
    print("OldPeak",oldPeak)
    print("Slope",slope)
    print("CA",ca)
    print("Thal",thal)
    print("=====================================")







    data = data[[
        "age",
        "sex",
        "chest_pain",
        "trestbps",
        "chol",
        "fbs",
        "restecg",
        "thalach",
        "exang",
        "oldpeak",
        "slope",
        "ca",
        "thal",
        "class"

    ]].dropna(axis=0, how='any')


    X_train, X_test = train_test_split(data, test_size=0.56, random_state=int(time.time()))
    gnb = GaussianNB()
    used_features = [
        "age",
        "sex",
        "chest_pain",
        "trestbps",
        "chol",
        "fbs",
        "restecg",
        "thalach",
        "exang",
        "oldpeak",
        "slope",
        "ca",
        "thal"

    ]
    gnb.fit(
        X_train[used_features].values,
        X_train["class"]
    )
    print(data.head())
    print("Dataset Lenght:: ", len(data))
    print("Dataset Shape:: ", data.shape)

    predict=gnb.predict([[age,sex,chest_pain,trestbps,chol,fbs,restEcg,thalach,exang,oldPeak,slope,ca,thal]])
    print("Predict Value",predict)


    if predict != 0:
        disease = Disease.objects.get(id=predict)
        prescribe = Prescribe(patient_id=id, disease_id=disease.id
                              )
        prescribe.save()

        user = User.objects.get(id=request.user.id)

        doctor = user.get_full_name()

        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages.create(

            body="Dear Patient-" + patient.firstname + " " + patient.lastname +"\n"+ "you have been diagnosed with -\n"+ disease.name+", Heart. "
                                                                                "Doctor name :: " + "" + doctor + "" + "" +
                 ":" + " ",
            to="+263774226217",
            from_="+18064513470", )
        print(message.body)

    else:
        disease = "Health"
    drugs = Drug.objects.all()



    context = {'predict': predict, 'patient': patient, 'drugs':drugs,'disease':disease,}
    template = loader.get_template('diagnosis.html')


    return HttpResponse(template.render(context, request))


# def prescribeDrug(request):
#
#     if not request.user.is_authenticated:
#         return redirect('home')
#
#
#     patient_id = request.POST.get('patient_id')
#
#     print(patient_id)
#     drug=request.POST['drug']
#     print("Drug ----------------------------------",drug)
#     Prescribe.objects.filter(Q(patient_id=patient_id)).update(drug_id=drug)
#
#
#     return redirect('view_patient_record', patient_id)


def create_disease(request):
    if not request.user.is_authenticated:
        return redirect('home')

    disease = Disease(name=request.POST['name'],description=request.POST['description'])

    disease.save()
    return redirect('read_disease')


def read_disease(request):
    if not request.user.is_authenticated:
        return redirect('home')
    diseases = Disease.objects.all()
    context = {'diseases': diseases}
    return render(request, 'disease/list.html', context)

def report(request):
    if not request.user.is_authenticated:
        return redirect('home')

    dataset = Prescribe.objects \
        .values('disease_id') \
        .annotate(d1=Count('disease_id', filter=Q(disease_id=1)),
                  d3=Count('disease_id', filter=Q(disease_id=3)),
                  d4=Count('disease_id', filter=Q(disease_id=4)),
                  d2=Count('disease_id', filter=Q(disease_id=2))) \
        .order_by('disease_id')

    categories = list()
    d1_series_data = list()
    d2_series_data = list()
    d3_series_data = list()
    d4_series_data = list()

    for entry in dataset:
        categories.append('%s Disease' % entry['disease_id'])
        d1_series_data.append(entry['d1'])
        d2_series_data.append(entry['d2'])
        d3_series_data.append(entry['d3'])
        d4_series_data.append(entry['d4'])

    d1_series = {
        'name': 'Angina Disease',
        'data': d1_series_data,
        'color': 'red'
    }

    d2_series = {
        'name': 'Coronary Artery Disease ',
        'data': d2_series_data,
        'color': 'green'
    }
    d3_series = {
        'name': 'Myocardial Infarction(Heart Attach)',
        'data': d3_series_data,
        'color': 'blue'
    }

    d4_series = {
        'name': 'Heart Failure',
        'data': d4_series_data,
        'color': 'black'
    }

    chart = {
        'chart': {'type': 'bar'},
        'title': {'text': 'Most Diagnosed Disease'},
        'xAxis': {'categories': categories},
        'series': [d1_series, d2_series,d3_series,d4_series]
    }



    dump = json.dumps(chart)

    return render(request, 'report/list.html', {'chart': dump})

def more_prescribed_drug(request):


    return  0

def prescribe_drug(request):

    if not request.user.is_authenticated:
        return redirect('home')


    disease_id = request.POST.get('disease_id')
    patient_id = request.POST.get('patient_id')
    print(disease_id)
    print(patient_id)
    drug=request.POST['drug']
    print("Drug ----------------------------------",drug)
    Prescribe.objects.filter(Q(patient_id=patient_id) & Q(disease_id=disease_id)).update(drug_id=drug)


    return redirect('view_patient_record', patient_id)