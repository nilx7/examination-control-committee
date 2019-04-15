from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from main_app.forms.main import EditAccountForm
from main_app.models import User
import re


def user_redirect(request):
    if request.user.Ins_ID.dept_set.exists():
        return HttpResponseRedirect('/hod/')
    else:
        return HttpResponseRedirect('/main/')


def change_password(request):
    account = request.user
    form = EditAccountForm(request.POST)

    context = {
        'form': form,
        'account': account,
    }
    if form.is_valid():
        user = authenticate(Ins_ID=account.Ins_ID,
                            password=form.cleaned_data['oldPassword'])
        if user is not None:
            if form.cleaned_data['newPassword'] == form.cleaned_data['confirmNewPassword']:
                if re.match(r'[A-Za-z0-9]{8,}', form.cleaned_data['newPassword']):
                    account.password = make_password(
                        form.cleaned_data['newPassword'])
                    account.save()
                    login(request, authenticate(Ins_ID=account.Ins_ID,
                                                password=form.cleaned_data['newPassword']))
                    messages.success(request, 'Password updated successfully')
                    return HttpResponseRedirect('/')
                else:
                    messages.error(
                        request, 'Password should be a combination of Alphabets and Numbers and more than 8 characters')
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, 'The new password does not match')
                return render(request, 'main.html', context)
        else:
            messages.error(request, 'The old password is wrong')
            return render(request, 'main.html', context)

    return render(request, 'main.html', context)


def main_view(request):
    if request.user.Ins_ID.dept_set.exists():
        return HttpResponseRedirect('/hod/')
    return render(request, 'main.html')


def custom404(request):
    return render(request, '404.html', status=404)


def custom500(request):
    return render(request, '500.html', status=500)
