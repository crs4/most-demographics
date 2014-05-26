from django import forms
from models import Patient, City, Identifier


class IdentifierForm(forms.Form):
    type = forms.CharField(max_length=50, required=False)
    domain = forms.CharField(max_length=50, required=False)
    identifier = forms.CharField(max_length=50)


class CityForm(forms.Form):
    name = forms.CharField(max_length=255)
    province = forms.CharField(max_length=2, required=False)
    state = forms.CharField(max_length=50)
    code = forms.CharField(max_length=5, required=False)


class PatientForm(forms.Form):
    account_number = forms.CharField(max_length=16)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    other_ids = forms.ModelMultipleChoiceField(queryset=Identifier.objects.all())
    gender = forms.ChoiceField(choices=Patient.GENDER_CHOICES)
    birth_date = forms.DateField() # input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d/%m/%Y', '%d-%m-%Y']
    birth_place = forms.ModelChoiceField(queryset=City.objects.all())
    address = forms.CharField(max_length=255, required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)
    phone = forms.CharField(max_length=20, required=False)
    mobile = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    certified_email = forms.EmailField(required=False)
    active = forms.BooleanField(required=False)
