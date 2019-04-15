import datetime

PERMISSION_CHOICES = (
    ('hod', 'Head of Department'),
    ('member', 'Examination Control Committee Member'),
    ('lecturer', 'Lecturer'),
    ('invigilator', 'Invigilator'),
)

LEVEL_CHOICES = (
    ('Fi', 'First'),
    ('SE', 'Seconed'),
    ('TH', 'Third'),
    ('FO', 'Fourth'),
    ('FI', 'Fifth'),
)

PERIOD_CHOICES = (
    ('First', '8:00 AM - 10:00 AM'),
    ('Seconed', '10:30 AM - 12:30 PM'),
    ('Third', '1:00 PM - 3:00 PM'),
)

YEAR_CHOICES = [(r,r) for r in range(2010, datetime.date.today().year+2)]

PERMISSION_FORM_CHOICES = (
    ('None', '----'),
    ('member', 'Examination Control Committee Member'),
    ('lecturer', 'Lecturer'),
    ('invigilator', 'Invigilator'),
)

ROLE_CHOICES = (
    ('invigilator', 'Invigilator'),
)

REPORT_FORM_CHOICES = (
    ('forgitId', 'Forgit ID Report'),
    ('phone', 'Phone Report'),
    ('Cheating', 'Cheating Report'),
)