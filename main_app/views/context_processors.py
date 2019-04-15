from main_app.forms.main import EditAccountForm


def change_password(request):
    return { 'form' :  EditAccountForm(request.POST)}