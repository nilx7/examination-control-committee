from django import forms

class LoginForm(forms.Form):
    employeeID = forms.IntegerField(label='Employee ID', min_value=0)
    password = forms.CharField(widget=forms.PasswordInput())