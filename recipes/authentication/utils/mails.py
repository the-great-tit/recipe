import os

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from celery.task import task


@task
def account_verification(email, token):
    email_subject = 'Verify your Recipes account'
    message = render_to_string('mail_templates/verify_account.html', {
        'domain': os.getenv('DOMAIN'),
        'token': token
    })

    to_email = email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.content_subtype = 'html'
    email.send()
