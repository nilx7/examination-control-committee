from django import forms


class EditAccountForm(forms.Form):
    oldPassword = forms.CharField(widget=forms.TextInput(attrs={'type':'password', 'class':'textinput textInput form-control is-invalid'}), label='Old Password')
    newPassword = forms.CharField(widget=forms.TextInput(attrs={'type':'password', 'class':'textinput textInput form-control is-invalid'}), label='New Password')
    confirmNewPassword = forms.CharField(widget=forms.TextInput(attrs={'type':'password', 'class':'textinput textInput form-control is-invalid'}), label='Confirm New Password')
