# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient, Bed, Doctor
from .filters import PatientFilter
import json

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid system credentials.')
            return redirect('login')
    return render(request, 'main/login.html')

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required(login_url='login')
def dashboard(request):
    active_status = ["Admitted", "Recovering", "Critical"]
    patients = Patient.objects.all()

    total_patients = patients.count()
    admitted_count = patients.filter(status__in=active_status).count()
    recovered_count = patients.filter(status__iexact="Discharged").count()
    deceased_count = patients.filter(status__iexact="Deceased").count()

    beds = list(Bed.objects.all())
    for bed in beds:
        bed.occupied = Patient.objects.filter(bed_num=bed, status__in=active_status).exists()
        bed.save()

    bed_labels = [b.bed_number for b in beds]
    bed_flags = [1 if b.occupied else 0 for b in beds]

    context = {
        'total_patients': total_patients,
        'admitted_count': admitted_count,
        'recovered_count': recovered_count,
        'deceased_count': deceased_count,
        'beds_available': Bed.objects.filter(occupied=False).count(),
        'beds_occupied': Bed.objects.filter(occupied=True).count(),
        'total_beds': len(beds),
        'beds': beds,
        'bed_labels_json': json.dumps(bed_labels),
        'bed_flags_json': json.dumps(bed_flags),
        'ward_labels_json': json.dumps(["OPD Bays", "General Wards", "ICU Suites", "Surge Reserves"]),
        'ward_total_json': json.dumps([25, 25, 25, 25]),
        'ward_occupied_json': json.dumps([0, 0, 0, 0]),
        'ward_free_json': json.dumps([25, 25, 25, 25]),
        'pie_labels_json': json.dumps(["Admitted", "Discharged Safely", "Deceased"]),
        'pie_data_json': json.dumps([admitted_count, recovered_count, deceased_count]),
    }
    return render(request, 'main/dashboard.html', context)

@login_required(login_url='login')
def add_patient(request):
    active_status = ["Admitted", "Recovering", "Critical"]
    free_beds = [b for b in Bed.objects.all() if not Patient.objects.filter(bed_num=b, status__in=active_status).exists()]
    doctors = Doctor.objects.filter(is_active_on_shift=True)

    if request.method == "POST":
        data = request.POST
        bed_obj = Bed.objects.get(id=data['bed_num'])
        doctor_obj = Doctor.objects.get(id=data['doctor'])

        Patient.objects.create(
            name=data['name'],
            phone_num=data['phone_num'],
            age=data['age'],
            patient_relative_name=data['patient_relative_name'],
            patient_relative_contact=data['patient_relative_contact'],
            address=data['address'],
            symptoms=data.getlist('symptoms'),
            prior_ailments=data['prior_ailments'],
            active_diagnosis=data['active_diagnosis'],
            ordered_diagnostics=data.get('ordered_diagnostics', 'None (Routine Triage)'),
            bill_amount=data.get('bill_amount', 0.00),
            bed_num=bed_obj,
            doctor=doctor_obj,
            status=data['status']
        )
        bed_obj.occupied = True
        bed_obj.save()
        return redirect('/')

    return render(request, 'main/add_patient.html', {"beds": free_beds, "doctors": doctors})

@login_required(login_url='login')
def patient(request, pk):
    patient_obj = get_object_or_404(Patient, id=pk)
    all_doctors = Doctor.objects.all()

    if request.method == "POST":
        data = request.POST
        old_bed = patient_obj.bed_num

        patient_obj.phone_num = data.get('mobile', patient_obj.phone_num)
        patient_obj.patient_relative_contact = data.get('mobile2', patient_obj.patient_relative_contact)
        patient_obj.patient_relative_name = data.get('relativeName', patient_obj.patient_relative_name)
        patient_obj.address = data.get('location', patient_obj.address)
        patient_obj.doctors_visiting_time = data.get('doctor_time', patient_obj.doctors_visiting_time)
        patient_obj.doctors_notes = data.get('doctor_notes', patient_obj.doctors_notes)
        patient_obj.age = data.get('age', patient_obj.age)
        patient_obj.active_diagnosis = data.get('active_diagnosis', patient_obj.active_diagnosis)
        patient_obj.ordered_diagnostics = data.get('ordered_diagnostics', patient_obj.ordered_diagnostics)
        patient_obj.bill_amount = data.get('bill_amount', patient_obj.bill_amount)
        
        new_status = data.get('status', patient_obj.status)
        patient_obj.status = new_status

        doctor_id = data.get('doctor')
        if doctor_id:
            patient_obj.doctor = Doctor.objects.get(id=doctor_id)

        patient_obj.save()

        if new_status in ["Discharged", "Deceased"]:
            if old_bed:
                old_bed.occupied = False
                old_bed.save()

        return redirect('/')

    return render(request, 'main/patient.html', {"patient": patient_obj, "doctors": all_doctors})

@login_required(login_url='login')
def patient_list(request):
    patients = Patient.objects.all()
    myFilter = PatientFilter(request.GET, queryset=patients)
    patients = myFilter.qs
    return render(request, 'main/patient_list.html', {"patients": patients, "myFilter": myFilter})

def info(request):
    return render(request, "main/info.html")

# Create your views here.
