from django import forms
from main_app.models import Course, Student
from django.utils.crypto import get_random_string
from main_app.choices import *

class AddReportForm(forms.Form):
    
    type_Of_Report = forms.ChoiceField(choices=REPORT_FORM_CHOICES)
    std_Id  = forms.IntegerField(label='Student ID', min_value=0)
    Descrption = forms.CharField(widget=forms.Textarea, required = False)
     