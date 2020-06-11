
@api_view(["POST"])
def professional_signin(request):
    email = request.data['email']
    password = request.data['password']
    data = {
        'username': email,
        'password': password
    }
    data = requests.post(f'{request.scheme}://{request.META["HTTP_HOST"]}/api/token/get/', json=data).json()
    user = User.objects.get(email=email)
    pro = Professional.objects.get(user_id = user.id)
    data['user'] = {
        'id' : user.id,
        'email' : email
    }
    data['pro'] = ProfessionalSerializer(pro, many=False).data
    response = Response(data)
    response.set_cookie('access', data["access"])
    response.set_cookie('refresh', data["refresh"])
    response.set_cookie('user', user.id)
    return response

@api_view(["POST"])
def company_signin(request):
    email = request.data['email']
    password = request.data['password']
    data = {
        'username': email,
        'password': password
    }
    data = requests.post(f'{request.scheme}://{request.META["HTTP_HOST"]}/api/token/get/', json=data).json()
    user = User.objects.get(email=email)
    company = Company.objects.get(user_id = user.id)
    data['user'] = {
        'id': user.id,
        'email': email
    }
    data['company'] = CompanySerializer(company, many=False).data
    response = Response(data)
    response.set_cookie('access', data["access"])
    response.set_cookie('refresh', data["refresh"])
    response.set_cookie('user', user.id)
    return response

                         
############################################################################################
                         
import base64
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
from rest_framework import parsers, renderers, generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from job.models import FavouriteJob, JobApplication
from job.serializers import SkillSerializer
from p7.auth import ProfessionalAuthentication, CompanyAuthentication
from p7.settings_dev import SITE_URL
from pro.serializers import *
from pro.serializers import ProfessionalSerializer
from pro.utils import sendSignupEmail, job_alert_save
from resources.strings_pro import *


@api_view(["POST"])
def profile_create_with_user_create(request):
    profile_data = json.loads(request.body)

    data_error = {
        'status': FAILED_TXT,
        'code': 500,
        "result": None
    }
    if 'email' not in profile_data:
        data_error["message"] = EMAIL_BLANK_ERROR_MSG
        return Response(data_error)
    if 'phone' not in profile_data:
        data_error["message"] = MOBILE_BLANK_ERROR_MSG
        return Response(data_error)
    if 'password' not in profile_data:
        data_error["message"] = PASSWORD_BLANK_ERROR_MSG
        return Response(data_error)

    try:
        user = User.objects.get(email=profile_data['email'])
        user_exist = True
        user_active = user.is_active
    except User.DoesNotExist:
        user_exist = False
        user_active = False

    try:
        pro = Professional.objects.get(email=profile_data['email'])
        pro_exist = True
    except Professional.DoesNotExist:
        pro_exist = False


    if user_exist and user_active:
        data_error["message"] = EMAIL_EXIST_ERROR_MSG
        return Response(data_error)

    hash_password = make_password(profile_data['password'])
    if not user_exist:
        user = User(email=profile_data['email'], password=hash_password, username=profile_data['email'], is_active=0)
        user.save()
        pro_group = Group.objects.get(name='Professional')
        user.groups.add(pro_group) # or using reverse relation pro_group.user_set.add(user)

    if not pro_exist:
        profile_data['terms_and_condition_status'] = 1 if profile_data['terms_and_condition_status'] == ON_TXT else 0
        profile_data['password'] = hash_password
        del profile_data['confirm_password']
        pro = Professional(**profile_data)
        pro.user_id = user.id
        if 'alert' in profile_data:
            pro.job_alert_status = True

        pro.save()

    sendSignupEmail(profile_data['email'],pro.id, datetime.date.today)

    data = {
        'status': 'success',
        'code': HTTP_200_OK,
        "message": 'success message here',  ## will change it later
        "result": {
            "user": {
                "email": profile_data['password'],
                "professional": pro.id
            }
        }
    }
    return Response(data)

                         
###################################################################################################################
                         
 @api_view(["GET"])
@permission_classes(())
def professional_signup_email_verification(request,token):
    # received_json_data = json.loads(request.body)
    email_start_marker = 'email='
    email_end_marker = '&token='
    email = token[token.find(email_start_marker)+len(email_start_marker):token.find(email_end_marker)]

    token_start_marker = 'token='
    token = token[token.find(token_start_marker)+len(token_start_marker):]
    print(email)
    print(token)

    try:
        professional=Professional.objects.get(email=email, signup_verification_code=token)
        professional.signup_verification_code= ''
        professional.save()
        user = User.objects.get(id=professional.user.id)
        user.is_active = 'True'
        user.save()
        status=HTTP_200_OK
    except Professional.DoesNotExist:
        status=HTTP_404_NOT_FOUND

    if status == HTTP_200_OK:
        message = PROFILE_VERIFICATION_SUCCESS_MESSAGE
    else:
        message = PROFILE_VERIFICATION_FAILED_MESSAGE

    return HttpResponseRedirect("/professional/sign-in/?{}".format(message))
