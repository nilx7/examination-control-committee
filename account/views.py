from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import LoginForm
from main_app.models import User



def has_perm(user):
    if user.Ins_ID.dept_set.exists() or user.is_member or user.Ins_ID.section_set.exists() or user.Ins_ID.control_set.exists():
        return True
    else:
        return False

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                u = form.cleaned_data['employeeID']
                p = form.cleaned_data['password']
                user = authenticate(Ins_ID=u, password=p)
                if user is not None:
                    if has_perm(user):
                        login(request, user)
                        messages.success(request, 'Successfully Logged In')
                        return HttpResponseRedirect('/')
                    else:
                        messages.error(
                            request, 'Sorry! Please contact your head of department.')
                        return HttpResponseRedirect('/')
                else:
                    messages.error(
                        request, 'Employee ID or Password not correct!')
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Something went wrong!')
                return HttpResponseRedirect('/')
        else:
            form = LoginForm()
            return render(request, 'account/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return HttpResponseRedirect('/')
