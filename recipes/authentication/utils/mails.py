import os

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from celery.task import task


@task
def auth_email(email, email_subject, email_template, token):
    """
    Email format for all authentication related emails
    :param email: the user's email
    :param email_subject: email subject
    :param email_template: html template to be used for the email
    :param token: generated token to identify the user
    :return: None
    """
    email_subject = email_subject
    message = render_to_string(email_template, {
        'domain': os.getenv('DOMAIN'),
        'token': token
    })

    to_email = email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.content_subtype = 'html'
    email.send()
