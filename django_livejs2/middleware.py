# Don't import unicode_literals here, otherwise set_cookie / delete_cookie will fail (as of django 1.4)
from __future__ import print_function

import hashlib
import re

from django.utils.http import http_date
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.contrib.staticfiles.handlers import StaticFilesHandler

HTML_CONTENT_TYPES = ("text/html", "application/xhtml+xml")
COOKIE_NAME = "DJANGO_LIVEJS2"

def inject_script_if_necessary(response):
    if (not hasattr(response, "content") or 
        getattr(response, "status_code", 0) != 200):

        return

    ctype = response.get("Content-Type", "").split(";")[0].strip().lower()
    if ctype not in HTML_CONTENT_TYPES:
        return

    src = getattr(settings,
                  "LIVEJS2_SCRIPT_SRC", 
                  settings.STATIC_URL + "django_livejs2/live.js")

    response.content = re.sub(
        r"(</head>)", 
        r"""<script type="text/javascript" src="{}"></script>\1""".format(src),
        response.content,
        count=1,
        flags=re.I,
    )

    if response.get("Content-Length", None):
        response["Content-Length"] = len(response.content)

def process(request, response):
    if request.GET.get("live", None) == "0":
        response.delete_cookie(COOKIE_NAME)
    elif (request.COOKIES.get(COOKIE_NAME, False) or
        request.GET.get("live", False)):

        # After a bit of thinking, I can't find any real use of this setting.
        # But since it has been written, just leave it here.
        cookie_age = getattr(settings,
                             "LIVEJS2_DISABLE_AFTER_INACTIVITY",
                             60*60*24*365*10)
        response.set_cookie(COOKIE_NAME, "1", max_age=cookie_age)

        inject_script_if_necessary(response)

        # We need to explicitly state that files are uncacheable, otherwise
        # Firefox (and possibly other browsers) may cache them for 1 minute
        response["Pragma"] = "no-cache"
        response["Cache-Control"] = "no-cache"
        response["Expires"] = http_date()
        if "ETag" not in response:
            response["ETag"] = '"{}"'.format(
                hashlib.md5(response.content).hexdigest()
            )

    return response

def patch_static_handler():
    # Static files won't go through middleware pipeline, so we have to do this
    old_serve = StaticFilesHandler.serve

    def _patched_serve(self, request):
        return process(request, old_serve(self, request))

    StaticFilesHandler.serve = _patched_serve

if settings.DEBUG:
    patch_static_handler()

class LiveJsMiddleware(object):
    def __init__(self):
        if not settings.DEBUG:
            raise MiddlewareNotUsed()

    def process_response(self, request, response):
        return process(request, response)
