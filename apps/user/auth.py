import logging

from django.conf import settings as conf_settings
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


class Permission(object):
    def not_logged_in(self, next=None):
        if next:
            return HttpResponseRedirect(conf_settings.LOGIN_URL + '?next=' + next)
        else:
            return HttpResponseRedirect(conf_settings.LOGIN_URL)


class LoginRequired(Permission):
    def dispatch(self, request, *args, **kwargs):
        header = request.session.get('Authorization', None)
        if not header or not header.startswith('Token '):
            return self.not_logged_in(next=request.get_full_path())

        token = header.split('Token ')[1]
        token = Token.objects.filter(key=token).first()
        if not token:
            return self.not_logged_in(next=request.get_full_path())

        user = token.user
        if not user.is_authenticated:
            return self.not_logged_in(next=request.get_full_path())

        return super(LoginRequired, self).dispatch(request, *args, **kwargs)


def get_loggedin_user(request):
    header = request.session.get('Authorization', None)
    if not header or not header.startswith('Token '):
        return None

    token = header.split('Token ')[1]
    token = Token.objects.filter(key=token).first()
    if not token:
        return None

    user = token.user
    if not user.is_authenticated:
        return None

    return user
