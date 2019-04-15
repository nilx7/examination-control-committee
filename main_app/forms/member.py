from django import forms
from main_app.models import User, Instructor, Control, Exam
from django.utils.crypto import get_random_string
from main_app.choices import *
import datetime


class DailyReportForm(forms.Form):
    today = datetime.date.today()
    Notes = forms.CharField(
        label="Notes", widget=forms.Textarea, required=False)
    Absents = forms.ModelMultipleChoiceField(label="Absents", queryset=Instructor.objects.filter(
        control__E_ID__Date__year=today.year, control__E_ID__Date__month=today.month, control__E_ID__Date__day=today.day).distinct(), widget=forms.CheckboxSelectMultiple, required=False)
    AbsentsNotes = forms.CharField(
        label="Notes about absents", widget=forms.Textarea, required=False)


class InvigilatorSchedulesForm(forms.Form):
    Ins_ID = forms.IntegerField(label='Employee ID', min_value=0)


class InvigilatorSwitchFirstForm(forms.Form):
    First_Ins_ID = forms.IntegerField(label='First Employee ID', min_value=0)
    Second_Ins_ID = forms.IntegerField(label='Second Employee ID', min_value=0)


class InvigilatorSwitchSecondForm(forms.Form):

    @staticmethod
    def label_from_instance(obj):
        course_instance = Exam.objects.values_list(
            'section__CCourse__CoName', flat=True).filter(pk=obj.E_ID.pk).first()
        date_instance = Exam.objects.values_list(
            'Date', flat=True).filter(pk=obj.E_ID.pk).first()
        rt = f'{course_instance} - ({date_instance})'
        return "%s" % rt

    def __init__(self, *args, **kwargs):
        a = kwargs.pop('first_ins_id', None)
        b = kwargs.pop('second_ins_id', None)
        super(InvigilatorSwitchSecondForm, self).__init__(*args, **kwargs)
        first_ins_query = Control.objects.filter(Ins_ID=a, Role='invigilator')
        second_ins_query = Control.objects.filter(Ins_ID=b, Role='invigilator')
        self.fields['First_Ins'].queryset = first_ins_query.exclude(
            E_ID__control__in=second_ins_query)
        self.fields['Second_Ins'].queryset = second_ins_query.exclude(
            E_ID__control__in=first_ins_query)
        self.fields['First_Ins'].label = f'Choose exam to switch for ({Instructor.objects.get(Ins_ID=a)})'
        self.fields['Second_Ins'].label = f'Choose exam to switch for ({Instructor.objects.get(Ins_ID=b)})'
        self.fields['First_Ins'].label_from_instance = self.label_from_instance
        self.fields['Second_Ins'].label_from_instance = self.label_from_instance
    First_Ins = forms.ModelMultipleChoiceField(queryset=None)
    Second_Ins = forms.ModelMultipleChoiceField(queryset=None)
