# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Executive Command Dashboard (Main Landing View)
    path('', views.dashboard, name='dashboard'),
    
    # System Session Access & Security
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Clinical Ingestion Triage & Patient Admission Panel
    path('add-patient/', views.add_patient, name='add_patient'),
    
    # Individual Electronic Health Record (EHR) Chart Profile
    path('patient/<int:pk>/', views.patient, name='patient'),
    
    # Inpatient Registry Search & Filter Directory Directory
    path('patient-list/', views.patient_list, name='patient_list'),
    
    # HK Corporate Clinical Infrastructure Capabilities Display
    path('info/', views.info, name='info'),
]