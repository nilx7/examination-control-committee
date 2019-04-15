from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from main_app.forms.invigilator import AddReportForm
from main_app.models import User, Exam, Control, Section, Instructor, Course, Dept, Problems, Takes, Student


@user_passes_test(lambda u: u.Ins_ID.control_set.exists())
def home_view(request):
    return render(request, 'invigilator/home.html')

#############################################################    Start view InvigilatorSchdule Functions    #############################################################


@user_passes_test(lambda u: u.Ins_ID.control_set.exists())
def Invigilator_Schdule_view(request):

    exams = Exam.objects.filter(control__Ins_ID=request.user.Ins_ID,
                                control__Role='invigilator').order_by('Date')  # instructor__

    context = {
        'exams': exams,
    }
    return render(request, 'invigilator/InvigilatorSchdules.html', context)


#############################################################    End Functions    #############################################################

#############################################################    Start view ProblemReport Functions    #############################################################

@user_passes_test(lambda u: u.Ins_ID.control_set.exists())
def invigilator_reports_view(request):
    today = datetime.date.today()

    problems = Problems.objects.all()
    exams = Exam.objects.filter(control__Ins_ID=request.user.Ins_ID, control__Role='invigilator',
                                Date__month=today.month, Date__day=today.day).order_by('Date')

    context = {
        'problems': problems,
        'exams': exams,
    }

    return render(request, 'invigilator/InvigilatorReports.html', context)


@user_passes_test(lambda u: u.Ins_ID.control_set.exists())
def add_report(request, E_ID):
    form = AddReportForm(request.POST)
    exam = Exam.objects.get(E_ID=E_ID)
    problems = Problems()
    context = {
        'form': form,
        'exam': exam,
    }
    if form.is_valid():
        std_pk = form.cleaned_data['std_Id']
        ins_pk = request.user.Ins_ID_id

        try:
            student_id = Student.objects.get(Std_ID=std_pk)
        except Student.DoesNotExist:
            messages.error(
                    request, 'Student does not exist!')
            return HttpResponseRedirect('/invigilator/InvigilatorReport')

        ins_ID = Instructor.objects.get(Ins_ID=ins_pk)
        E_ID = Exam.objects.get(E_ID=E_ID)
        if student_id is not None:
            if Takes.objects.filter(Std_ID=student_id.pk, Sec_ID__E_ID=E_ID.pk).exists():
                problems.Type = form.cleaned_data['type_Of_Report']
                problems.Std_ID = student_id
                problems.Ins_ID = ins_ID
                problems.E_ID = E_ID
                problems.Describtion = form.cleaned_data['Descrption']
                problems.save()
                messages.success(
                    request, 'Successfully created report')
                return HttpResponseRedirect('/invigilator/InvigilatorReport')
            else:
                messages.error(
                    request, 'Student does not take the course or number incorrect!')
                return HttpResponseRedirect('/invigilator/InvigilatorReport')
    return render(request, 'invigilator/cud/AddReportForm.html', context)

#############################################################    End Functions    #############################################################
