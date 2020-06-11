import random
import string
from django.utils.text import slugify
from job import models
# Random string generator


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Unique Slug Generator
def unique_slug_generator(instance, new_slug=None):
    """
    It assumes your instance has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        job_id = str(instance.job_id)
        slug = "{slug}-{uuid}".format(slug=slugify(instance.title), uuid = job_id[-8:])

    Klass = instance.__class__

    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
# Unique Slug Generator

# Favourite Job Counter
def favourite_job_counter(job):
    """
    It assumes your instance has a model with a slug field and a title character (char) field.
    """
    if job:
        fav_job = models.FavouriteJob.objects.filter(job=job).count()
        job.favorite_count = fav_job
        job.save()
# Favourite Job Counter

# Applied Job Counter
def applied_job_counter(job):
    """
    It assumes your instance has a model with a slug field and a title character (char) field.
    """
    if job:
        app_job = models.JobApplication.objects.filter(job=job).count()
        job.applied_count = app_job
        job.save()
# Applied Job Counter


################################################################################################################

from difflib import SequenceMatcher

from django.core.mail import send_mail
from django.template import loader

from p7.settings_dev import *
from pro.models import Professional


def sendSignupEmail(email,id, date):
    # unique_id = random.randint(100000, 999999)
    # updateExamineeVerficationCode(email, unique_id)
    id=str(id)
    date = str(date)
    activation_link = hash(id+date)
    updateProfessionalVerficationLink(email, activation_link)

    data = ''
    html_message = loader.render_to_string(
        'account_activation_email.html',
        {
            'activation_url': "{}/api/professional/signup-email-verification/email={}&token={}".format(SITE_URL, email, activation_link),
            'activation_email': email,
            'subject': 'Thank you from' + data,
        }
    )
    subject_text = loader.render_to_string(
        'account_activation_email_subject.txt',
        {
            'user_name': email,
            'subject': 'Thank you from' + data,
        }
    )

    message = ' it  means a world to us '
    email_from = EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject_text, message, email_from, recipient_list,html_message=html_message)

def updateProfessionalVerficationLink(email, unique_link):
    professional = Professional.objects.get(email=email)
    professional.signup_verification_code = unique_link
    professional.save()

def job_alert_save(email):
    user = Professional.objects.get(email = email)
    user.job_alert_status = True
    user.save()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
