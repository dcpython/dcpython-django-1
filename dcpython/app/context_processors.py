# encoding: utf-8


def path_hierarchy(request):
    """Make it easy for templates to access URL path components"""
    return {'PATH_HIERARCHY': filter(None, request.path.strip('/').split('/')) }
