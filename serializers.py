from rest_framework import serializers
from .models import Company, Job, Industry, JobType, Experience, Qualification, Gender, Currency, TrendingKeywords, \
    Skill, JobSource, JobCategory, JobGender, JobApplication
from rest_framework.validators import *


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, label='company_name')
    # contact_no = serializers.CharField(required=True, max_length=11)
    email = serializers.CharField(max_length=30, validators=[UniqueValidator(queryset=Company.objects.all())])

    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {'client': {'required': False}}

class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CompanyProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['profile_picture']

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['name']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name']

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ['name']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['name']

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['name']

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['name']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class JobSerializer(serializers.ModelSerializer):
    is_favourite = serializers.BooleanField(read_only=True)
    is_applied = serializers.BooleanField(read_only=True)
    company = CompanySerializer(many=False)
    class Meta:
        model = Job
        fields = ('job_id', 'title', 'status' , 'company', 'job_category',
                  'application_deadline', 'job_area', 'job_city', 'job_country',
                  'job_site', 'job_nature', 'job_type',
                  'created_at', 'post_date', 'slug', 'applied_count', 'favorite_count',
                  'is_applied', 'is_favourite', 'vacancy' , 'address', 'company')


class JobSerializerAllField(serializers.ModelSerializer):
    is_favourite = serializers.CharField(read_only=True)
    is_applied = serializers.CharField(read_only=True)
    company = CompanySerializer(many=False)
    job_skills = SkillSerializer(many=True)
    class Meta:
        model = Job
        fields = '__all__'

class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = ['name']

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['name']

class JobGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobGender
        fields = ['name']

# TODO: remove if not needed
class RecentJobSerializer(serializers.ModelSerializer):
    status = serializers.CharField()

    class Meta:
        model = Job
        fields = ['job_location', 'job_id', 'company', 'employment_status', 'title', 'created_date', 'status']


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'web_address', 'company_profile']

class TrendingKeywordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingKeywords
        fields = ['keyword']

class TopCategoriesSerializer(serializers.ModelSerializer):
    num_posts = serializers.IntegerField(read_only=True)
    class Meta:
        model = JobCategory
        fields= ['name', 'num_posts']

class TopCompanySerializer(serializers.ModelSerializer):
    num_posts = serializers.IntegerField(read_only=True)
    class Meta:
        model = Company
        fields= ['name', 'num_posts']



class TopSkillSerializer(serializers.ModelSerializer):
    skills_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Skill
        fields= '__all__'

class TopJobSerializer(serializers.ModelSerializer):
    favourite_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Job
        fields= ['title','favourite_count']


class JobApplicationShortListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['is_shortlisted']
