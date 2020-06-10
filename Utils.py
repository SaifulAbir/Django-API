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
