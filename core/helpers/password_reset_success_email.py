from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_password_reset_success_email(user_email):
    html_content = render_to_string('password_reset_success_email_template.html')

    email = EmailMessage(
        subject="Password Reset Successful",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
    )
    email.content_subtype = 'html'
    email.send()
