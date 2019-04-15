from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from threading import Thread

from main_app.sender import *
from main_app.forms.lecturer import *
from main_app.models import Submission, Section


@user_passes_test(lambda u: u.Ins_ID.section_set.exists())
def home_view(request):
    return render(request, 'lecturer/home.html')

#############################################################    Start Functions    #############################################################


@user_passes_test(lambda u: u.Ins_ID.section_set.exists())
def submit_exam_view(request):
    sections = Section.objects.filter(
        Ins_ID=request.user.Ins_ID,
    ).order_by('E_ID__Date')

    paginator = Paginator(sections, 10)
    section_pages = request.GET.get('page')
    sections = paginator.get_page(section_pages)
    context = {
        'sections': sections,
    }
    return render(request, 'lecturer/SubmitExam.html', context)


@user_passes_test(lambda u: u.Ins_ID.section_set.exists())
def redirect_submit_exam(request, pk):
    section = get_object_or_404(Section, pk=pk, Ins_ID=request.user.Ins_ID)

    form = SubmitExamForm(request.POST)
    request.session['typesOfCalc'] = None
    request.session['notes'] = None
    context = {
        'section': section,
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            request.session['noModels'] = form.cleaned_data['noModels']
            request.session['noOfPapers'] = form.cleaned_data['noOfPapers']
            request.session['noOfDN'] = form.cleaned_data['noOfDN']
            request.session['typesOfCalc'] = form.cleaned_data['typesOfCalc']
            request.session['notes'] = form.cleaned_data['notes']
            submission = Submission(
                Ins_ID = request.user.Ins_ID,
                ID = section,
            )
            submission.save()
            return HttpResponseRedirect(f'/lecturer/SubmitExam/Form/{pk}')
    return render(request, 'lecturer/cud/RedirectSubmitExam.html', context)


@user_passes_test(lambda u: u.Ins_ID.section_set.exists())
def submit_exam_form(request, pk):

    noModels = request.session.get('noModels')
    noOfPapers = request.session.get('noOfPapers')
    typesOfCalc = request.session.get('typesOfCalc')
    noOfDN = request.session.get('noOfDN')
    notes = request.session.get('notes')

    section = get_object_or_404(Section, pk=pk, Ins_ID=request.user.Ins_ID)
    context = {
        'section': section,
        'noModels': noModels,
        'noOfPapers': noOfPapers,
        'typesOfCalc': typesOfCalc,
        'noOfDN': noOfDN,
        'notes': notes,
    }

    html = render_to_string('lecturer/forms/CoverForm.html', context)
    thread = Thread(target=pdf_mail, args=(html, 'coverform', [request.user.Ins_ID.Email]))
    thread.start()

    return render(request, 'lecturer/forms/CoverForm.html', context)


@user_passes_test(lambda u: u.Ins_ID.section_set.exists())
def confirm_delivering_view(request):
    submitted = Submission.objects.filter(
        Ins_ID=request.user.Ins_ID,
    ).order_by('D_Status')

    paginator = Paginator(submitted, 10)
    submitted_page = request.GET.get('page')
    submitted = paginator.get_page(submitted_page)
    context = {
        'submitted': submitted,
    }
    return render(request, 'lecturer/ConfirmDelivering.html', context)


@user_passes_test(lambda u: u.Ins_ID.section_set.exists())
def confirm_delivering(request, pk):
    submission = get_object_or_404(
        Submission, pk=pk, Ins_ID=request.user.Ins_ID)
    context = {
        'submission': submission,
    }
    if request.method == 'POST':
        submission.D_Status = True
        submission.save()
        message = """
Exam : ({}) has been confirmed delivering by: ({})

Examination Control Committee""".format(submission.ID.CCourse.CoName, submission.Ins_ID)
        mail_thread = Thread(target=send_mail, args=(message, [submission.Member_ID.Email]))
        mail_thread.start()
        # sms_thread = Thread(target=send_sms, args=(message,))
        # sms_thread.start()
        messages.success(request, 'Successfully confirmed delivering')
        return HttpResponseRedirect('/lecturer/ConfirmDelivering')
    return render(request, 'lecturer/cud/ConfirmDeliver.html', context)


@user_passes_test(lambda u: u.Ins_ID.section_set.exists())
def remove_submission(request, pk):
    submitted = get_object_or_404(
        Submission, pk=pk, Ins_ID=request.user.Ins_ID)
    context = {
        'submitted': submitted,
    }
    if request.method == 'POST':
        if not submitted.S_Status:
            submitted.delete()
            messages.success(request, 'Successfully remove submission')
        else:
            messages.error(request, 'You can not remove!')
        return HttpResponseRedirect('/lecturer/ConfirmDelivering')
    return render(request, 'lecturer/cud/RemoveSubmission.html', context)

#############################################################    End Functions    #############################################################
