from django import forms


class SubmitExamForm(forms.Form):
    noModels = forms.IntegerField(label='No. of models', widget= forms.TextInput(attrs={'type' : 'number', 'value': '2', 'min':'0'}), min_value=0)
    noOfPapers = forms.IntegerField(label='No. of copies/Model',widget= forms.TextInput(attrs={'type' : 'number', 'value': '30', 'min':'0'}), min_value=0)
    noOfDN = forms.IntegerField(label='No. of DN students',widget= forms.TextInput(attrs={'type' : 'number', 'value': '0', 'min':'0'}), min_value=0)
    typesOfCalc = forms.CharField(label="Type of calculator (if any)",widget= forms.TextInput(attrs={'value': 'No calculator'}), required=False)
    notes = forms.CharField(label="Extra notes", widget=forms.Textarea, required=False)
