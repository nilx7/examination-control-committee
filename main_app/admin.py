from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import *

admin.site.unregister(Group)

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        import_id_fields = ('Std_ID',)

class CollegeResource(resources.ModelResource):
    class Meta:
        model = College
        import_id_fields = ('CCollege',)

class DeptResource(resources.ModelResource):
    class Meta:
        model = Dept
        import_id_fields = ('Dcode',)

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
        import_id_fields = ('CoCourse',)

class InstructorResource(resources.ModelResource):
    class Meta:
        model = Instructor
        import_id_fields = ('ID',)

class SectionResource(resources.ModelResource):
    class Meta:
        model = Section
        import_id_fields = ('Ins_ID',)

class ExamResource(resources.ModelResource):
    class Meta:
        model = Exam
        import_id_fields = ('E_ID',)


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    pass

@admin.register(College)
class CollegeAdmin(ImportExportModelAdmin):
    resource_class = CollegeResource
    pass
@admin.register(Dept)
class DeptAdmin(ImportExportModelAdmin):
    resource_class = DeptResource
    pass

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
    pass

@admin.register(Instructor)
class InstructorAdmin(ImportExportModelAdmin):
    resource_class = InstructorResource
    pass

@admin.register(Section)
class SectionAdmin(ImportExportModelAdmin):
    resource_class = SectionResource
    pass

@admin.register(Exam)
class ExamAdmin(ImportExportModelAdmin):
    resource_class = ExamResource
    pass

@admin.register(Room)
class RoomAdmin(ImportExportModelAdmin):
    pass

@admin.register(Inst_Phone)
class Inst_PhoneAdmin(ImportExportModelAdmin):
    pass

@admin.register(Std_Phone)
class Std_PhoneAdmin(ImportExportModelAdmin):
    pass

@admin.register(Takes)
class TakesAdmin(ImportExportModelAdmin):
    pass

@admin.register(Control)
class ControlAdmin(ImportExportModelAdmin):
    pass

@admin.register(Has)
class HasAdmin(ImportExportModelAdmin):
    pass

@admin.register(Problems)
class ProblemsAdmin(ImportExportModelAdmin):
    pass

@admin.register(Submission)
class SubmissionAdmin(ImportExportModelAdmin):
    pass