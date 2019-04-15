import weasyprint
from django.conf import settings
from django.core.mail import EmailMessage
import datetime


def send_mail(message, to_list):
    mail = EmailMessage('Examination Control Committee', message, settings.EMAIL_HOST_USER, to_list)
    mail.send()
    return print('Successfully sent email')

#   Send forms as PDF
def pdf_mail(html, attach_name, to_list):
    pdf = weasyprint.HTML(string=html).write_pdf()
    mail = EmailMessage('Examination Control Committee', '', settings.EMAIL_HOST_USER, to_list)
    mail.attach(f"{attach_name}-{datetime.date.today()}.pdf", pdf, "application/pdf")
    mail.send()
    return print('Successfully PDF generated and sent')

def send_sms(message):
    settings.SMS_CLIENT.send_message({'from': 'ECC', 'to': '+9665', 'text': message})
    return print('Successfully sent SMS')

    