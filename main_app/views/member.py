from django.forms.formsets import formset_factory
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.conf import settings
from threading import Thread
from django.template.loader import render_to_string
import datetime

from main_app.forms.member import *
from main_app.models import Instructor, Exam, Control, Section, Submission, Inst_Phone, Problems
from main_app.choices import PERIOD_CHOICES
from main_app.sender import *


@user_passes_test(lambda u: u.is_member == True)
def home_view(request):
    return render(request, 'member/home.html')

#############################################################    Start Functions    #############################################################


@user_passes_test(lambda u: u.is_member == True)
def invigilator_schedules(request):
    form = InvigilatorSchedulesForm(request.POST)
    context = {
        'form': form,
    }
    if form.is_valid():
        ins_id = form.cleaned_data['Ins_ID']
        instructor = Instructor.objects.filter(Ins_ID=ins_id)
        schedules = Exam.objects.filter(
            control__Ins_ID=ins_id, control__Role='invigilator')
        if instructor.exists() and schedules.count() > 0:
            context = {
                'form': form,
                'instructor': instructor,
                'schedules': schedules,
            }
            return render(request, 'member/InvigilatorSchedules.html', context)
        else:
            messages.error(
                request, 'Sorry! There are no schedules for this instructor or employee id wrong')
            return HttpResponseRedirect('/member/InvigilatorSchedules')

    return render(request, 'member/InvigilatorSchedules.html', context)


@user_passes_test(lambda u: u.is_member == True)
def invigilator_switch(request):
    form = InvigilatorSwitchFirstForm(request.POST)
    context = {
        'form': form,
    }
    if form.is_valid():
        first_ins_id = form.cleaned_data['First_Ins_ID']
        second_ins_id = form.cleaned_data['Second_Ins_ID']
        return HttpResponseRedirect(f'/member/InvigilatorSwitch/{first_ins_id}-{second_ins_id}')
    return render(request, 'member/InvigilatorSwitch.html', context)


@user_passes_test(lambda u: u.is_member == True)
def invigilator_switching(request, pk1, pk2):
    first_ins = Instructor.objects.filter(Ins_ID=pk1)
    second_ins = Instructor.objects.filter(Ins_ID=pk2)
    if not first_ins.exists() or not second_ins.exists():
        messages.error(
            request, 'Sorry! One or both of employees id doesn\'t exist.')
        return HttpResponseRedirect('/member/InvigilatorSwitch')
    if pk1 == pk2:
        messages.error(
            request, 'Sorry! Please enter two different employees ID.')
        return HttpResponseRedirect('/member/InvigilatorSwitch')

    form = InvigilatorSwitchSecondForm(
        request.POST, first_ins_id=pk1, second_ins_id=pk2)
    first_ins_schedule = Exam.objects.filter(
        control__Ins_ID=pk1, control__Role='invigilator')
    second_ins_schedule = Exam.objects.filter(
        control__Ins_ID=pk2, control__Role='invigilator')

    context = {
        'form': form,
        'first_ins_schedule': first_ins_schedule,
        'second_ins_schedule': second_ins_schedule,
        'first_ins': first_ins,
        'second_ins': second_ins,
    }

    if form.is_valid():
        first_ins_control = Control.objects.get(
            Ins_ID=form.cleaned_data['First_Ins'].values()[0]['Ins_ID_id'],
            E_ID=form.cleaned_data['First_Ins'].values()[0]['E_ID_id'],
        )
        second_ins_control = Control.objects.get(
            Ins_ID=form.cleaned_data['Second_Ins'].values()[0]['Ins_ID_id'],
            E_ID=form.cleaned_data['Second_Ins'].values()[0]['E_ID_id'],
        )
        temp = first_ins_control.Ins_ID
        first_ins_control.Ins_ID = second_ins_control.Ins_ID
        second_ins_control.Ins_ID = temp
        first_ins_control.save()
        second_ins_control.save()
        messages.success(request, 'Successfully invigilator switched')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'member/InvigilatorSwitching.html', context)


@user_passes_test(lambda u: u.is_member == True)
def all_invigilator_schedules(request):
    instructors = Instructor.objects.filter(
        control__Role='invigilator').distinct()
    if instructors.count() > 0:
        context = {
            'instructors': instructors,
        }
        return render(request, 'member/AllInvigilatorSchedules.html', context)
    else:
        messages.error(
            request, 'Sorry! There are no schedules')
        return HttpResponseRedirect('/member/InvigilatorSchedules')
    return render(request, 'member/AllInvigilatorSchedules.html', context)


@user_passes_test(lambda u: u.is_member == True)
def exam_schedules(request):
    # sections = Section.objects.all()
    exams = Exam.objects.all().order_by('Date')
    context = {
        'exams': exams,
    }

    return render(request, 'member/ExamSchedules.html', context)


@user_passes_test(lambda u: u.is_member == True)
def exam_submission_view(request):
    submissions = Submission.objects.filter(
        Ins_ID__Dcode=request.user.Ins_ID.Dcode,
        S_Status=False,
        D_Status=False,
        Member_ID=None,
    )
    paginator = Paginator(submissions, 10)
    submissions_page = request.GET.get('page')
    submissions = paginator.get_page(submissions_page)
    context = {
        'submissions': submissions,
    }

    return render(request, 'member/ExamSubmission.html', context)


@user_passes_test(lambda u: u.is_member == True)
def exam_submission(request, pk):
    if Submission.objects.filter(pk=pk, Ins_ID__Dcode=request.user.Ins_ID.Dcode, S_Status=False, D_Status=False, Member_ID=None).exists():
        submission = get_object_or_404(Submission, pk=pk)
        context = {
            'submission': submission,
        }
        if request.method == 'POST':
            submission.S_Status = True
            submission.Member_ID = request.user.Ins_ID
            submission.save()
            message = """
Exam : ({}) has been confirmed submission by: ({})

Examination Control Committee""".format(submission.ID.CCourse.CoName, request.user.Ins_ID)
            mail_thread = Thread(target=send_mail, args=(
                message, [submission.Ins_ID.Email]))
            mail_thread.start()
            # sms_thread = Thread(target=send_sms, args=(message,))
            # sms_thread.start()
            messages.success(request, 'Successfully confirmed submission')
            return HttpResponseRedirect('/member/ExamSubmission')
    else:
        return HttpResponseRedirect('/member/ExamSubmission')
    return render(request, 'member/cud/ConfirmSubmission.html', context)


@user_passes_test(lambda u: u.is_member == True)
def deliver_exams_view(request):
    submitted = Submission.objects.filter(
        Ins_ID__Dcode=request.user.Ins_ID.Dcode,
        S_Status=True,
        Member_ID=request.user.Ins_ID,
    ).order_by('D_Status')

    paginator = Paginator(submitted, 10)
    submitted_page = request.GET.get('page')
    submitted = paginator.get_page(submitted_page)
    context = {
        'submitted': submitted,
    }
    return render(request, 'member/DeliverExams.html', context)


@user_passes_test(lambda u: u.is_member == True)
def undo_submission(request, pk):
    if Submission.objects.filter(pk=pk, Member_ID=request.user.Ins_ID).exists():
        submitted = get_object_or_404(Submission, pk=pk)
        context = {
            'submitted': submitted,
        }
        if request.method == 'POST':
            if not submitted.D_Status:
                submitted.S_Status = False
                submitted.Member_ID = None
                submitted.save()
                messages.success(request, 'Successfully undo submission')
            else:
                messages.error(request, 'You can not undo!')
            return HttpResponseRedirect('/member/DeliverExams')
    else:
        return HttpResponseRedirect('/member/DeliverExams')
    return render(request, 'member/cud/UndoSubmission.html', context)


@user_passes_test(lambda u: u.is_member == True)
def reports_problem(request):

    problems = Problems.objects.all().order_by('-id')

    context = {
        'problems': problems,
    }

    return render(request, 'member/reports.html', context)


@user_passes_test(lambda u: u.is_member == True)
def phone_report_view(request, id):

    problem = Problems.objects.get(id=id)

    context = {
        'problem': problem,
    }

    return render(request, 'member/forms/phoneReport.html', context)


@user_passes_test(lambda u: u.is_member == True)
def forgit_id_report_view(request, id):

    problem = Problems.objects.get(id=id)

    context = {
        'problem': problem,
    }
    return render(request, 'member/forms/forgitIdReport.html', context)


@user_passes_test(lambda u: u.is_member == True)
def cheating_report_view(request, id):
    problem = Problems.objects.get(id=id)

    context = {
        'problem': problem,
    }
    return render(request, 'member/forms/cheatingReport.html', context)

#############################################################    End Functions    #############################################################


@user_passes_test(lambda u: u.is_member == True)
def daily_report_view(request):
    form = DailyReportForm(request.POST)
    today = datetime.date.today()
    today_exams = Exam.objects.filter(
        Date__year=today.year, Date__month=today.month, Date__day=today.day)
    print(today_exams.count())
    if today_exams.count() <= 0:
        messages.error(request, 'There are no exams today!')
        return HttpResponseRedirect('/member/')
    request.session['SubmitTimes'] = 1
    request.session['Notes'] = None
    request.session['Absents'] = None
    request.session['AbsentsNotes'] = None

    if request.method == "POST":
        if form.is_valid():
            request.session['Notes'] = form.cleaned_data['Notes']
            absents_query = form.cleaned_data['Absents'].values()
            request.session['Absents'] = list(absents_query)
            request.session['AbsentsNotes'] = form.cleaned_data['AbsentsNotes']
            return HttpResponseRedirect('/member/DailyReportForm/')

    context = {
        'form': form,
    }
    return render(request, 'member/DailyReport.html', context)


@user_passes_test(lambda u: u.is_member == True)
def daily_report_form(request):
    today = datetime.date.today()
    today_exams = Exam.objects.filter(
        Date__year=today.year, Date__month=today.month, Date__day=today.day)
    inst_phones = Inst_Phone.objects.all()
    if today_exams.count() <= 0:
        messages.error(request, 'There are no exams today!')
        return HttpResponseRedirect('/member/DailyReport/')
    members = User.objects.filter(is_member=True)
    Notes = request.session.get('Notes')
    Absents = request.session.get('Absents')
    AbsentsNotes = request.session.get('AbsentsNotes')

    context = {
        'exams': today_exams,
        'today_date': today,
        'Periods': PERIOD_CHOICES,
        'members': members,
        'Notes': Notes,
        'Absents': Absents,
        'AbsentsNotes': AbsentsNotes,
        'inst_phones': inst_phones,
    }
    html = render_to_string('member/forms/DailyReport.html', context)
    thread = Thread(target=pdf_mail, args=(html, 'dailyreport',
                                           [request.user.Ins_ID.Dcode.Ins_ID.Email]))
    thread.start()

    return render(request, 'member/forms/DailyReport.html', context)
