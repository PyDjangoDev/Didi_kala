from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_email(subject , to , context , template_name):
    try:
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, text_content, from_email,[to], html_message=html_content)
        return True
    
    except Exception as err:
        print(err)
        return False
    
    