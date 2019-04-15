from django import forms
from main_app.models import User, Instructor, Dept
from main_app.choices import *


class AddAccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        req_user_dcode = kwargs.pop('req_user_dcode', None)
        super(AddAccountForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = Instructor.objects.filter(
            user__isnull=True).filter(Dcode=req_user_dcode)

    instructor = forms.ModelChoiceField(queryset=None)
    password = forms.CharField(widget=forms.PasswordInput())


class AddMemberForm(forms.Form):
    def __init__(self, *args, **kwargs):
        req_user_dcode = kwargs.pop('req_user_dcode', None)
        check_hod_query = Dept.objects.values('Ins_ID').exclude(Ins_ID=None)
        super(AddMemberForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Instructor.objects.filter(
            user__isnull=False, user__is_member=False).filter(Dcode=req_user_dcode).exclude(Ins_ID__in=check_hod_query)

    account = forms.ModelChoiceField(queryset=None)


class EditPermissionForm(forms.Form):
    permission = forms.ChoiceField(choices=PERMISSION_FORM_CHOICES,)
