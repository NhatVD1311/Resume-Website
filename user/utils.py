from datetime import date
from io import BytesIO
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import *


def match_skill(job_list, skill_list, preferred_job_list):
    recommendation_list = []
    for skill in skill_list:
        for job in job_list:
            split_text = skill.skill_title.lower().split(' ')

            for s in split_text:
                index = job.requirements.lower().find(s)
                index1 = job.job_title.lower().find(s)

                if (index >= 0 or index1 >= 0) and job not in recommendation_list:
                    recommendation_list.append(job)

    for preferred_job in preferred_job_list:
        for job in job_list:
            split_text = preferred_job.details.lower().split(' ')

            for s in split_text:
                index = job.requirements.lower().find(s)
                index1 = job.job_title.lower().find(s)
                if (index >= 0 or index1 >= 0) and job not in recommendation_list:
                    recommendation_list.append(job)

    return recommendation_list


def rateAvg(rates, length):
    summation = 0
    if length == 0:
        return 0
    else:
        for r in rates:
            summation = summation + r.rate

    if (summation / length) % 1 > 0:
        return summation / length
    else:
        return summation // length


def increaseViewCount(user_one, user_two):
    if user_one.is_company:
        applicant = ApplicantProfileModel.objects.get(user=user_two)
        if applicant.totalViewCount is None:
            applicant.totalViewCount = 0
        applicant.totalViewCount = applicant.totalViewCount + 1
        applicant.save()
    elif user_one.is_applicant:
        company = CompanyProfileModel.objects.get(user=user_two)
        if company.totalViewCount is None:
            company.totalViewCount = 0
        company.totalViewCount = company.totalViewCount + 1
        company.save()

    ProfileViewDetails.objects.create(
        viewedBy=user_one,
        viewed=user_two,
    )
    return


def extractFirstName(name):
    first_name = name.split(' ')
    return first_name[0]


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def add_to_employee_keyword(user, keyword):
    if keyword is not None:
        EmployeeSearchKeywordModel.objects.create(
            searched_by=user,
            searched_for=keyword,
        )
    return


def add_to_job_keyword(user, keyword):
    if keyword is not None:
        JobSearchKeywordModel.objects.create(
            searched_by=user,
            searched_for=keyword,
        )
    return


def deactivate_user(user):
    user.is_active = False
    user.save()
    return

