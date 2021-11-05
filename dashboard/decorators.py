import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.http import HttpResponse


def group_required(group, login_url='/useraccount/common_login', raise_exception=False):
    def check_params(user):
        if isinstance(group, six.string_types):
            groups = (group,)
        else:
            groups=group
        if user.groups.filter(name__in=groups).exists():
            return True

        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_params, login_url=login_url)