from rest_framework_simplejwt.authentication import JWTAuthentication

from p7.models import is_professional, is_company


class P7Authentication(JWTAuthentication):
    def authenticate(self, request):
        return super(P7Authentication, self).authenticate(request)

class ProfessionalAuthentication(P7Authentication):
    def authenticate(self, request):
        result = super(ProfessionalAuthentication, self).authenticate(request)
        if result is not None:
            user = result[0]
            if is_professional(user):
                return result
        return None

class CompanyAuthentication(P7Authentication):
    def authenticate(self, request):
        result = super(CompanyAuthentication, self).authenticate(request)
        if result is not None:
            user = result[0]
            if is_company(user):
                return result
        return None
