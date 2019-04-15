from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
from threading import Thread
import re

from main_app.sender import *
from main_app.forms.hod import *
from main_app.models import User, Instructor, Inst_Phone, Exam


@user_passes_test(lambda u: u.Ins_ID.dept_set.exists())
def home_view(request):
    return render(request, 'hod/home.html')

#############################################################    Start Manage Accounts Functions    #############################################################


@user_passes_test(lambda u: u.Ins_ID.dept_set.exists())
def manage_accounts_view(request):
    get_search = request.GET.get('Ins_Search')
    if get_search is not None and get_search.isnumeric():
        accounts = User.objects.filter(
            Ins_ID__Dcode=request.user.Ins_ID.Dcode, Ins_ID=request.GET.get('Ins_Search'))
    else:
        accounts = User.objects.filter(Ins_ID__Dcode=request.user.Ins_ID.Dcode)
    paginator = Paginator(accounts, 10)
    page = request.GET.get('page')
    accounts = paginator.get_page(page)
    context = {
        'accounts': accounts,
    }
    return render(request, 'hod/ManageAccounts.html', context)


@user_passes_test(lambda u: u.Ins_ID.dept_set.exists())
def add_account(request):
    form = AddAccountForm(
        request.POST, req_user_dcode=request.user.Ins_ID.Dcode)
    context = {
        'form': form,
    }
    if form.is_valid():
        if re.match(r'[A-Za-z0-9]{8,}', form.cleaned_data['password']):
            user = User(
                Ins_ID=form.cleaned_data['instructor'],
                password=make_password(form.cleaned_data['password']),
            )
            user.save()
            user = User.objects.get(
                Ins_ID=form.cleaned_data['instructor'])  # Email
    #         message = """
    # Dear: {}
    # An account has been created for you.
    # password: {}

    # Examination Control Committee""".format(
    #             form.cleaned_data['instructor'], form.cleaned_data['password'])
    #         mail_thread = Thread(target=send_mail, args=(message, [user.Ins_ID.Email]))
    #         mail_thread.start()
            # sms_thread = Thread(target=send_sms, args=(message,))
            # sms_thread.start()
            messages.success(
                request, 'Successfully created account: {}'.format(user.Ins_ID))
            return HttpResponseRedirect('/hod/ManageAccounts')
        else:
            messages.error(
                request, 'Password should be a combination of Alphabets and Numbers and more than 8 characters')
            return HttpResponseRedirect('/hod/ManageAccounts')

    return render(request, 'hod/cud/AddAccount.html', context)


@user_passes_test(lambda u: u.Ins_ID.dept_set.exists())
def delete_account(request, pk):
    account = get_object_or_404(User, pk=pk)
    context = {
        'account': account,
    }
    if request.method == 'POST':
        #         message = """
        # Your account has been deleted.

        # Examination Control Committee"""
        account.delete()
        # mail_thread = Thread(target=send_mail, args=(message, [account.Ins_ID.Email]))
        # mail_thread.start()
        # sms_thread = Thread(target=send_sms, args=(message,))
        # sms_thread.start()
        messages.success(
            request, 'Successfully deleted account')
        return HttpResponseRedirect('/hod/ManageAccounts')
    return render(request, 'hod/cud/DeleteAccount.html', context)

#############################################################   End Manage Accounts Functions   #############################################################


#############################################################   Start Manage Permissions Functions  #############################################################

@user_passes_test(lambda u: u.Ins_ID.dept_set.exists())
def manage_members_view(request):
    get_search = request.GET.get('Ins_Search')
    if get_search is not None and get_search.isnumeric():
        accounts = User.objects.filter(Ins_ID=get_search, is_member=True)
    else:
        accounts = User.objects.filter(is_member=True)
    paginator = Paginator(accounts, 10)
    page = request.GET.get('page')
    accounts = paginator.get_page(page)
    context = {
        'accounts': accounts,
    }
    return render(request, 'hod/ManageMembers.html', context)


@user_passes_test(lambda u: u.Ins_ID.dept_set.exists())
def add_member(request):
    form = AddMemberForm(
        request.POST, req_user_dcode=request.user.Ins_ID.Dcode)
    context = {
        'form': form,
    }
    if form.is_valid():
        account = User.objects.get(Ins_ID=form.cleaned_data['account'])
        account.is_member = True
        account.save()
        messages.success(
            request, 'Successfully added member: {}'.format(account.Ins_ID))
        return HttpResponseRedirect('/hod/ManageMembers')
    return render(request, 'hod/cud/AddMember.html', context)


@user_passes_test(lambda u: u.Ins_ID.dept_set.exists())
def remove_member(request, pk):
    account = get_object_or_404(User, pk=pk)
    context = {
        'account': account,
    }
    if (request.method == "POST"):
        account.is_member = False
        account.save()
        messages.success(
            request, 'Successfully remove member: {}'.format(account.Ins_ID))
        return HttpResponseRedirect('/hod/ManageMembers')
    return render(request, 'hod/cud/RemoveMember.html', context)


#############################################################   End Manage Permissions Functions    #############################################################
