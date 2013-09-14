# -*- encoding: utf-8 -*-
import codecs
import sys
from django.utils.translation import ugettext as _, gettext

writer_factory = codecs.getwriter("utf-8")
sys.stdout = writer_factory(sys.stdout)

from xmodule.modulestore.django import modulestore
from xmodule.course_module import CourseDescriptor
from django.conf import settings



def pick_subdomain(domain, options, default='default'):
    for option in options:
        if domain.startswith(option):
            return option
    return default

#hung add
def position(str):
    size=len(str)
    i=0
    list=[]
    for x in str:
        if x=='/':
            list.append(i)
        i=i+1
    return list

#hung add
def searchIndex(str,value,uni=None,cousre=None,course_name=None):


    a=position(str)
    if uni is not None:
        if (str.find(value,0,a[0]))!=-1:
            return 1
        else:
            return -1
    if cousre is not None:
        if (str.find(value,a[0]+1,a[1]))!=-1:
            return 1
        else:
            return -1
    if course_name is not None:
        str=str.upper().lstrip()
        if (str.find(value.upper().lstrip()))!=-1:
            return  1
        else:
            return -1
    else:
            return 0



def get_course_by_courseid(course_id,uni=None,courseId=None,courseName=None,domain=None):
    """
    Return the set of CourseDescriptors that should be visible in this branded instance
    """

    _course=modulestore().get_courses()
    # _course=get_visible_courses(domain=None)
    datalist=[]
    for value in _course:

        if uni is not None:
            if (searchIndex(value.id,course_id,uni=1))==1:
                datalist.append(value)
        elif courseId is not None:
            if (searchIndex(value.id,course_id,cousre=1))==1:
                datalist.append(value)
        elif courseName is not None:


            if (searchIndex(value.display_name_with_default,course_id,course_name=1))==1:

                datalist.append(value)


    courses = [c for c in datalist
               if isinstance(c, CourseDescriptor)]
    courses = sorted(courses, key=lambda course: course.number)

    if domain and settings.MITX_FEATURES.get('SUBDOMAIN_COURSE_LISTINGS'):
        subdomain = pick_subdomain(domain, settings.COURSE_LISTINGS.keys())
        visible_ids = frozenset(settings.COURSE_LISTINGS[subdomain])

        return [course for course in courses if course.id in visible_ids]
    else:

        return courses


def get_visible_courses(domain=None):
    """
    Return the set of CourseDescriptors that should be visible in this branded instance
    """

    _course=modulestore().get_courses()

    courses = [c for c in _course
               if isinstance(c, CourseDescriptor)]
    courses = sorted(courses, key=lambda course: course.number)

    if domain and settings.MITX_FEATURES.get('SUBDOMAIN_COURSE_LISTINGS'):
        subdomain = pick_subdomain(domain, settings.COURSE_LISTINGS.keys())
        visible_ids = frozenset(settings.COURSE_LISTINGS[subdomain])

        return [course for course in courses if course.id in visible_ids]
    else:

        return courses


def get_university(domain=None):
    """
    Return the university name specified for the domain, or None
    if no university was specified
    """
    if not settings.MITX_FEATURES['SUBDOMAIN_BRANDING'] or domain is None:
        return None

    subdomain = pick_subdomain(domain, settings.SUBDOMAIN_BRANDING.keys())
    return settings.SUBDOMAIN_BRANDING.get(subdomain)


def get_logo_url(domain=None):
    """
    Return the url for the branded logo image to be used
    """
    university = get_university(domain)

    if university is None:
        return '/static/images/header-logo.png'

    return '/static/images/{uni}-on-edx-logo.png'.format(
        uni=university
    )
