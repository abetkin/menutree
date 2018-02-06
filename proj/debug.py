
import sys
from contextlib import ExitStack
from django.conf import settings


class DebugMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if not settings.DEBUG:
            return
        from ipdb import post_mortem
        e, m, tb = sys.exc_info()
        print(m.__repr__(), file=sys.stderr)
        post_mortem(tb)
