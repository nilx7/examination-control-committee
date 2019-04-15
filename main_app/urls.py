from django.urls import path
from .views import main, hod, member, lecturer, invigilator
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #############################################################   Main    #############################################################
    path('', login_required(main.user_redirect), name='user_redirect'),
    path('main/', login_required(main.main_view), name='main'),
    path('404/', main.custom404, name='404'),
    path('500/', main.custom500, name='500'),
    path('main/ChangePassword/', login_required(main.change_password), name='ChangePassword'),

    #############################################################   Head of Department  #############################################################
    path('hod/', login_required(hod.home_view), name='HodHome'),
    path('hod/ManageAccounts/', login_required(hod.manage_accounts_view), name='ManageAccounts'),
    path('hod/ManageAccounts/AddAccount/', login_required(hod.add_account), name='AddAccount'),
    path('hod/ManageAccounts/DeleteAccount/<int:pk>/', login_required(hod.delete_account), name='DeleteAccount'),
    path('hod/ManageMembers/', login_required(hod.manage_members_view), name='ManageMembers'),
    path('hod/ManageMembers/AddMember/', login_required(hod.add_member), name='AddMember'),
    path('hod/ManageMembers/RemoveMember/<int:pk>', login_required(hod.remove_member), name='RemoveMember'),

    #############################################################   Examination Control Member  #############################################################
    path('member/', login_required(member.home_view), name='MemberHome'),
    path('member/InvigilatorSchedules', login_required(member.invigilator_schedules), name='InvigilatorSchedules'),
    path('member/InvigilatorSwitch', login_required(member.invigilator_switch), name='InvigilatorSwitch'),
    path('member/InvigilatorSwitch/<int:pk1>-<int:pk2>', login_required(member.invigilator_switching), name='InvigilatorSwitching'),
    path('member/AllInvigilatorSchedules', login_required(member.all_invigilator_schedules), name='AllInvigilatorSchedules'),
    path('member/ExamSchedules', login_required(member.exam_schedules), name='ExamSchedules'),
    path('member/ExamSubmission', login_required(member.exam_submission_view), name='ExamSubmission'),
    path('member/ExamSubmission/ConfirmSubmission/<int:pk>/', login_required(member.exam_submission), name='ConfirmSubmission'),
    path('member/DeliverExams', login_required(member.deliver_exams_view), name='DeliverExams'),
    path('member/ExamSubmission/UndoSubmission/<int:pk>/', login_required(member.undo_submission), name='UndoSubmission'),
    path('member/DailyReport/', login_required(member.daily_report_view), name='DailyReport'),
    path('member/DailyReportForm/', login_required(member.daily_report_form), name='DailyReportForm'),
    path('member/reportsProblem/', login_required(member.reports_problem), name='reportsProblem'),
    path('member/reportsProblem/phoneReport/<int:id>/', login_required(member.phone_report_view), name='phoneReport'),
    path('member/reportsProblem/forgitIdReport/<int:id>/', login_required(member.forgit_id_report_view), name='forgitIdReport'),
    path('member/reportsProblem/cheatingReport/<int:id>/', login_required(member.cheating_report_view), name='cheatingReport'),

    #############################################################   Lecturer    #############################################################
    path('lecturer/', login_required(lecturer.home_view), name='LecturerHome'),
    path('lecturer/SubmitExam/', login_required(lecturer.submit_exam_view), name='SubmitExam'),
    path('lecturer/SubmitExam/redirect/<int:pk>', login_required(lecturer.redirect_submit_exam), name='RedirectSubmitExam'),
    path('lecturer/SubmitExam/Form/<int:pk>', login_required(lecturer.submit_exam_form), name='SubmitExamForm'),
    path('lecturer/ConfirmDelivering', login_required(lecturer.confirm_delivering_view), name='ConfirmDelivering'),
    path('lecturer/ConfirmDelivering/ConfirmDeliver/<int:pk>/', login_required(lecturer.confirm_delivering), name='ConfirmDeliver'),
    path('lecturer/ConfirmDelivering/RemoveSubmission/<int:pk>/', login_required(lecturer.remove_submission), name='RemoveSubmission'),

    #############################################################   Invigilator #############################################################
    path('invigilator/', login_required(invigilator.home_view), name='InvigilatorHome'),
    path('invigilator/InvigilatorReport', login_required(invigilator.invigilator_reports_view), name='InvigilatorReport'),
    path('invigilator/InvigilatorSchdules', login_required(invigilator.Invigilator_Schdule_view), name='InvigilatorSchdules'),
    path('invigilator/InvigilatorReport/AddReport/<int:E_ID>', login_required(invigilator.add_report), name='AddReport'),

]

handler404 = 'main.custom404'
handler500 = 'main.custom500'
