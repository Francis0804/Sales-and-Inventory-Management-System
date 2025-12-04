import threading

_thread_locals = threading.local()

class CurrentUserMiddleware:
    """Middleware that stores the current request user in thread-local storage.

    This allows signal handlers and other code without direct request access to
    determine the acting user when processing requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            _thread_locals.user = getattr(request, 'user', None)
        except Exception:
            _thread_locals.user = None
        response = self.get_response(request)
        return response


def get_current_user():
    return getattr(_thread_locals, 'user', None)
