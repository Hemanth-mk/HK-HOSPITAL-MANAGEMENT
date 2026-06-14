# main/models.py
from django.db import models
from multiselectfield import MultiSelectField

class Doctor(models.Model):
    """
    Advanced Specialized Consultant Registry tracking 30+ medical specialties.
    """
    SPECIALTY_CHOICES = [
        ('PRIMARY_CARE', 'Primary & General Care (GP / Family Physician)'),
        ('CARDIOLOGY', 'Cardiology (Heart & Vascular Specialists)'),
        ('DERMATOLOGY', 'Dermatology (Skin, Hair & Nails)'),
        ('ENDOCRINOLOGY', 'Endocrinology (Hormones & Metabolism)'),
        ('GASTROENTEROLOGY', 'Gastroenterology (Digestive & Liver)'),
        ('NEUROLOGY', 'Neurology (Brain & Nervous System)'),
        ('PULMONOLOGY', 'Pulmonology (Respiratory & Lung Care)'),
        ('NEPHROLOGY', 'Nephrology (Kidney Health & Dialysis)'),
        ('RHEUMATOLOGY', 'Rheumatology (Joint & Autoimmune)'),
        ('GEN_SURGERY', 'General Surgery (Abdominal & Soft Tissue)'),
        ('ORTHOPEDICS', 'Orthopedics (Musculoskeletal & Bones)'),
        ('NEUROSURGERY', 'Neurosurgery (Brain & Spine Surgical)'),
        ('OBGYN', 'Obstetrics & Gynecology (OB/GYN)'),
        ('OPHTHALMOLOGY', 'Ophthalmology (Vision Care & Surgery)'),
        ('ENT', 'Otolaryngology (Ear, Nose & Throat)'),
        ('EMERGENCY', 'Emergency Medicine Specialists (ER)'),
        ('CRITICAL_CARE', 'Critical Care / ICU Specialists'),
        ('RADIOLOGY', 'Radiology (Imaging Diagnostics)'),
        ('PATHOLOGY', 'Pathology (Advanced Laboratory Medicine)'),
        ('PSYCHIATRY', 'Psychiatry (Mental Health Services)'),
        ('PHYSIOTHERAPY', 'Physiotherapy & Rehabilitation Unit'),
        ('INFECTIOUS_DISEASE', 'Infectious Disease Isolation Unit'),
    ]

    name = models.CharField(max_length=100)
    specialty_branch = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, default='PRIMARY_CARE')
    qualification = models.CharField(max_length=50, default="MBBS, MD")
    is_active_on_shift = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.qualification} - {self.get_specialty_branch_display()})"


class Bed(models.Model):
    """
    100-Unit Master Resource Fleet.
    25 OPD Bays, 25 General Wards, 25 ICU Suites, 25 Surge Reserves.
    """
    WARD_CHOICES = [
        ('OPD', 'OPD Daycare / Minor Triage Bay (25 Beds)'),
        ('GENERAL', 'General Medical Inpatient Ward (25 Beds)'),
        ('ICU', 'High-Tier Intensive Trauma ICU Suite (25 Beds)'),
        ('RESERVE', 'Dynamic Surge Expansion Reserve Ward (25 Beds)'),
    ]

    bed_number = models.CharField(max_length=50, unique=True)
    ward_type = models.CharField(max_length=30, choices=WARD_CHOICES, default='GENERAL')
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Bed {self.bed_number} [{self.get_ward_type_display()}]"


class Patient(models.Model):
    """
    Comprehensive Electronic Health Record (EHR) Clinical Ledger.
    """
    name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=15)
    age = models.IntegerField(default=30)
    patient_relative_name = models.CharField(max_length=50, null=True, blank=True)
    patient_relative_contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField()

    CLINICAL_MANIFEST = (
        ('Fever', 'Fever'), ('Headache', 'Headache'), ('Body pain', 'Body pain'), 
        ('Fatigue', 'Fatigue'), ('Cold', 'Cold'), ('Cough', 'Cough'), 
        ('Vomiting', 'Vomiting'), ('Diarrhea', 'Diarrhea'), ('Skin rash', 'Skin rash'), 
        ('Loss of appetite', 'Loss of appetite'), ('Chest pain', 'Chest pain'), 
        ('Palpitations', 'Palpitations'), ('Shortness of breath', 'Shortness of breath'), 
        ('Swollen legs', 'Swollen legs'), ('Dizziness', 'Dizziness'), ('Fainting', 'Fainting'),
        ('Itching', 'Itching'), ('Skin redness', 'Skin redness'), ('Dry skin', 'Dry skin'), 
        ('Hair loss', 'Hair loss'), ('Acne', 'Acne'), ('Pigmentation', 'Pigmentation'),
        ('Excessive thirst', 'Excessive thirst'), ('Weight gain', 'Weight gain'), 
        ('Weight loss', 'Weight loss'), ('Increased urination', 'Increased urination'),
        ('Stomach pain', 'Stomach pain'), ('Bloating', 'Bloating'), ('Acid reflux', 'Acid reflux'),
        ('Severe headache', 'Severe headache'), ('Memory loss', 'Memory loss'), 
        ('Numbness', 'Numbness'), ('Seizures', 'Seizures'), ('Wheezing', 'Wheezing'), 
        ('Breathing difficulty', 'Breathing difficulty'), ('Chest tightness', 'Chest tightness'),
        ('Swelling', 'Swelling'), ('Reduced urine', 'Reduced urine'), ('Blood in urine', 'Blood in urine'), 
        ('High BP', 'High BP'), ('Joint pain', 'Joint pain'), ('Joint swelling', 'Joint swelling'), 
        ('Stiffness', 'Stiffness'), ('Abdominal pain', 'Abdominal pain'), ('Hernia bulge', 'Hernia bulge'), 
        ('Trauma', 'Trauma'), ('Bone pain', 'Bone pain'), ('Difficulty walking', 'Difficulty walking'), 
        ('Head injury', 'Head injury'), ('Brain tumor symptoms', 'Brain tumor symptoms'), 
        ('Paralysis', 'Paralysis'), ('Pelvic pain', 'Pelvic pain'), ('Irregular periods', 'Irregular periods'), 
        ('Pregnancy complications', 'Pregnancy complications'), ('Blurred vision', 'Blurred vision'), 
        ('Eye pain', 'Eye pain'), ('Red eye', 'Red eye'), ('Ear pain', 'Ear pain'), 
        ('Hearing loss', 'Hearing loss'), ('Sore throat', 'Sore throat'), ('Nasal blockage', 'Nasal blockage'),
        ('Severe bleeding', 'Severe bleeding'), ('Unconsciousness', 'Unconsciousness'), ('Poisoning', 'Poisoning'),
    )
    symptoms = MultiSelectField(choices=CLINICAL_MANIFEST, null=True, blank=True)
    active_diagnosis = models.TextField(default="Pending Evaluation Verification")
    prior_ailments = models.TextField(blank=True, default="None")
    ordered_diagnostics = models.CharField(max_length=250, default="None (Routine Triage)")

    bed_num = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    
    admission_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    doctors_notes = models.TextField(null=True, blank=True, default="Clinical admission evaluation complete.")
    doctors_visiting_time = models.CharField(max_length=50, default="09:00 AM - 11:30 AM")
    status = models.CharField(max_length=50, default='Admitted')

    def __str__(self):
        return f"{self.name} - [{self.status}]"