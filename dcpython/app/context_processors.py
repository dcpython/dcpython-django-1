# encoding: utf-8
from django.conf import settings

def path_hierarchy(request):
    """ Make it easy for templates to access URL path components """
    return {'PATH_HIERARCHY': filter(None, request.path.strip('/').split('/')) }

def google_analytics(request):
	""" Make it easy for templates to access google analytics key """
	return {'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID}