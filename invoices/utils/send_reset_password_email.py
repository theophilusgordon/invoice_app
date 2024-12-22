from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_reset_password_email(user_email, reset_link):
    html_content = render_to_string('reset_password_email_template.html', {'reset_link': reset_link})

    email = EmailMessage(
        subject="Password Reset Request",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
    )
    email.content_subtype = 'html'
    email.send()
