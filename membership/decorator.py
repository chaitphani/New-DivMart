from .models import *
from django.shortcuts import redirect


def is_authenticated(f):
    def wrap(request, *args, **kwargs):
        # this will check the session if userid key exist, if not it will redirect to login page
        try:
            user_obj = RegisteredMembers.objects.filter(email=request.session['email']) | RegisteredMembers.objects.filter(self_ref_id=request.session['email'])
        except Exception as e:
            print('--exception as e in decorator-----', e)
            user_obj = False
        if 'email' in request.session.keys() and user_obj:
            return f(request, *args, **kwargs)
        request.session.clear()
        return redirect("member-login")

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap