# main/filters.py
import django_filters
from .models import Patient

class PatientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Patient Name")
    status = django_filters.ChoiceFilter(
        choices=[
            ('Admitted', 'Admitted'),
            ('Recovering', 'Recovering'),
            ('Critical', 'Critical'),
            ('Discharged', 'Discharged Safely'),
            ('Deceased', 'Deceased Logged'),
        ],
        label="Clinical Care Status"
    )

    class Meta:
        model = Patient
        fields = ['name', 'status']