from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    AbstractUser,
)
from django.contrib.auth.models import PermissionsMixin

from main_app.choices import *
from django.utils.translation import ugettext_lazy as _
import datetime


class MyUserManager(BaseUserManager):
    def create_user(self, Ins_ID, password=None):
        if not Ins_ID:
            raise ValueError('Users must have an instructor')

        user = self.model(
            Ins_ID=Instructor.objects.get(pk=Ins_ID),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Ins_ID, password):
        user = self.create_user(
            Ins_ID,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    Ins_ID = models.OneToOneField(
        'Instructor', on_delete=models.CASCADE, verbose_name='Instructor ID')
    is_staff = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    
    objects = MyUserManager()

    USERNAME_FIELD = 'Ins_ID'

    def __str__(self):
        return '{}'.format(self.Ins_ID)


class Student(models.Model):
    Std_ID = models.IntegerField(primary_key=True, verbose_name='Student ID')
    Fname = models.CharField(max_length=60, verbose_name='First Name')
    Minit = models.CharField(max_length=60, verbose_name='Middle Name')
    Lname = models.CharField(max_length=60, verbose_name='Last Name')
    Dcode = models.ForeignKey('Dept', on_delete=models.CASCADE,
                              blank=True, null=True, verbose_name='Department Code')
                              
    def getName(self):
        return '{} {} {}'.format(self.Fname, self.Minit, self.Lname)

    def __str__(self):
        return '{} {}'.format(self.Std_ID, self.Fname)


class College(models.Model):
    CCollege = models.IntegerField(
        primary_key=True, verbose_name='College Code')
    Cname = models.CharField(max_length=160, verbose_name='College Name')

    def __str__(self):
        return '{} - {}'.format(self.Cname, self.CCollege)


class Dept(models.Model):
    Dcode = models.IntegerField(
        primary_key=True, verbose_name='Department Code')
    Dname = models.CharField(max_length=255, verbose_name='Department Name')
    CCollege = models.ForeignKey(
        'College', on_delete=models.CASCADE, blank=True, null=True, verbose_name='College Code')
    Ins_ID = models.ForeignKey('Instructor', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name='Instructor ID')

    def __str__(self):
        return '{}'.format(self.Dname)


class Course(models.Model):
    CoCourse = models.CharField(
        primary_key=True, max_length=15, verbose_name='Course Code')
    CoName = models.CharField(max_length=255, verbose_name='Course Name')
    Level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    Dcode = models.ForeignKey(
        Dept, on_delete=models.CASCADE, verbose_name='Department Code')

    def __str__(self):
        return '{}'.format(self.CoName,)


class Instructor(models.Model):
    Ins_ID = models.IntegerField(
        primary_key=True, verbose_name='Instructor ID')
    Fname = models.CharField(max_length=60, verbose_name='First Name')
    Minit = models.CharField(max_length=60, verbose_name='Middle Name', null=True)
    Lname = models.CharField(max_length=60, verbose_name='Last Name')
    Rank = models.CharField(max_length=60)
    Email = models.EmailField(
        max_length=70, null=True, blank=True, unique=True)
    Dcode = models.ForeignKey('Dept', on_delete=models.CASCADE,
                              blank=True, null=True, verbose_name='Department Code')

    def __str__(self):
        if not self.Minit:
            return '{} {}'.format(self.Fname, self.Lname)
        else:
            return '{} {} {}'.format(self.Fname, self.Minit, self.Lname)


class Section(models.Model):
    class Meta:
        unique_together = (
            ('CCourse', 'Ins_ID'),
        )
    ID = models.IntegerField(primary_key=True, verbose_name='Section ID')
    Name = models.CharField(max_length=60, verbose_name='Section Name')
    Semester = models.CharField(max_length=60)
    year = models.IntegerField(
        _('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    CCourse = models.ForeignKey(
        'Course', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Course Code')
    Ins_ID = models.ForeignKey('Instructor', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name='Instructor ID')
    E_ID = models.ForeignKey(
        'Exam', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Exam ID')

    def __str__(self):
        return '{} {}'.format(self.Name, self.CCourse)


class Exam(models.Model):
    E_ID = models.AutoField(primary_key=True, verbose_name='Exam ID')
    Period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    Date = models.DateField()

    def __str__(self):
        return '{} {}'.format(self.Period, self.Date)


class Room(models.Model):
    class Meta:
        unique_together = (
            ('BLDG', 'Room'),
        )
    BLDG = models.CharField(max_length=60, verbose_name='Bulding Number')
    Room = models.CharField(max_length=60)
    Size = models.IntegerField()

    def __str__(self):
        return 'Bulding:{}, Room:{}, Size:{}'.format(self.BLDG, self.Room, self.Size)


class Inst_Phone(models.Model):
    Ins_ID = models.ForeignKey('Instructor', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name='Instructor ID')
    Phone_number = models.CharField(
        max_length=14, unique=True, verbose_name='Phone Number')

    def __str__(self):
        return '{} -> {}'.format(self.Ins_ID, self.Phone_number)


class Std_Phone(models.Model):
    Std_ID = models.ForeignKey(
        'Student', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Student ID')
    Phone_number = models.CharField(
        max_length=14, unique=True, verbose_name='Phone Number')

    def __str__(self):
        return '{} -> {}'.format(self.Std_ID, self.Phone_number)


class Takes(models.Model):
    class Meta:
        unique_together = (
            ('Std_ID', 'Sec_ID'),
        )
    Std_ID = models.ForeignKey(
        'Student', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Student ID')
    Sec_ID = models.ForeignKey(
        'Section', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Section ID')

    def __str__(self):
        return '{} at Section:{}'.format(self.Std_ID, self.Sec_ID)


class Control(models.Model):
    class Meta:
        unique_together = (
            ('Ins_ID', 'E_ID'),
        )
    Ins_ID = models.ForeignKey('Instructor', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name='Instructor ID')
    E_ID = models.ForeignKey(
        'Exam', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Exam ID')
    Role = models.CharField(
        max_length=60, choices=ROLE_CHOICES, verbose_name='Role')

    def __str__(self):
        return 'Ins:{}, Exam:{}, Role:{}'.format(self.Ins_ID, self.E_ID, self.Role)


class Has(models.Model):
    class Meta:
        unique_together = (
            ('Room', 'E_ID'),
        )
    Room = models.ForeignKey(
        'Room', on_delete=models.CASCADE, blank=True, null=True)
    E_ID = models.ForeignKey(
        'Exam', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Exam ID')

    def __str__(self):
        return '{} has exam:{}'.format(self.Room, self.E_ID)


class Problems(models.Model):
    Type = models.CharField(max_length=15, default=None, blank=True, null=True, choices=REPORT_FORM_CHOICES)
    Std_ID = models.ForeignKey(
        'Student', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Student ID')
    Ins_ID = models.ForeignKey('Instructor', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name='Instructor ID')
    E_ID = models.ForeignKey(
        'Exam', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Exam ID')
    Describtion = models.TextField()

    def __str__(self):
        return 'Student:{}, Ins:{}, Exam:{}, Description:{}'.format(self.Std_ID, self.Ins_ID, self.E_ID, self.Describtion)


class Submission(models.Model):
    Ins_ID = models.ForeignKey('Instructor', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name='Instructor ID')
    ID = models.ForeignKey(
        'Section', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Section ID')
    S_Status = models.BooleanField(
        default=False, verbose_name='Submission status')
    D_Status = models.BooleanField(
        default=False, verbose_name='Delivery status')
    Member_ID = models.ForeignKey('Instructor', on_delete=models.CASCADE,
                                  blank=True, null=True, related_name='Member_ID+', verbose_name='Examination Control Member ID')

    def __str__(self):
        return '{} , {} - status(S,D): {},{} By: {}'.format(self.Ins_ID, self.ID, self.S_Status, self.D_Status, self.Member_ID)
