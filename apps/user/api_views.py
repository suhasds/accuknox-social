import re
from threading import Thread

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView, status

from apps.user.models import User, UserProfile
from apps.user.utils import send_mail
from apps.user.auth import get_loggedin_user

from apps.commons.status_codes import *
from main.settings import settings
import uuid


def create_user_and_profile(email, name, user_group='users', password=None, picture=None):
    user = User(email=email)
    user.set_password(password)
    user.save()

    user_profile = UserProfile(name=name, user=user, picture=picture)
    user_profile.save()

    # Set user group as user
    user_group = Group.objects.get_or_create(name=user_group)[0]
    user.groups.add(user_group)
    user.save()

    return user, user_profile


class SignUpAPI(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name', None)
        password = data.get('password', None)
        email = data.get('email', None)
        picture = request.FILES.get('picture', None)
        user_group = data.get('user_group', 'users')

        if not name or not password or not email or not user_group:
            return Response(UserStatusCodes.MISSING_FIELDS_FOR_REGISTRATION, status=status.HTTP_412_PRECONDITION_FAILED)

        email = email.lower()

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response(UserStatusCodes.INVALID_EMAIL, status=status.HTTP_400_BAD_REQUEST)

        existing_user = User.objects.filter(email=email).count()
        if existing_user:
            return Response(UserStatusCodes.SAME_USER_EXISTS, status=status.HTTP_200_OK)

        user, user_profile = create_user_and_profile(email, name, user_group, password, picture)

        response = UserStatusCodes.REGISTRATION_SUCCESS
        response['data'] = {
            'user': user.to_dict()
        }
        return Response(response, content_type='json', status=status.HTTP_200_OK)


class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        if email is None or password is None:
            return Response(UserStatusCodes.LOGIN_FAILED, status=status.HTTP_412_PRECONDITION_FAILED)

        user = authenticate(email=email.lower(), password=password)
        if not user:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        user_profile = UserProfile.objects.filter(user=user).first()
        if not user_profile.email_verified:
            return Response(UserStatusCodes.EMAIL_NOT_VERIFIED, status=status.HTTP_200_OK)

        if user.is_active and not user.is_admin:  # user should be active and should not be admin
            token, created = Token.objects.get_or_create(user=user)
            response = AppAuthStatusCodes.USER_FOUND
            response['data'] = {
                'token': token.key
            }
            request.session['Authorization'] = 'Token ' + token.key
            request.session['user_id'] = str(user.record_id)
            return Response(response, status=status.HTTP_200_OK)

        # else if user is not active or not found
        return Response(UserStatusCodes.LOGIN_FAILED, status=status.HTTP_200_OK)


class LogoutAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.auth.pk
        if not token:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        Token.objects.filter(key=token).delete()
        return Response(UserStatusCodes.USER_LOGGED_OUT, status=status.HTTP_200_OK)


class ForgotPasswordAPI(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        if not email:
            return Response(AppAuthStatusCodes.MISSING_FIELDS_FOR_RESET, status=status.HTTP_200_OK)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        new_password = str(uuid.uuid1())
        user.set_password(new_password)
        user.save()

        # Notify the end_user with the updated password
        to_email = email
        subject = 'Password Reset'
        text_message = '''
             Hello,\n\n

             We have reset your password and your new password is {new_password}\n\n

             You can now login using your login email and the new password from {login_url}.
         '''.format(new_password=new_password, login_url=settings.DOMAIN_URL + settings.LOGIN_URL)

        html_message = '''
                     Hello,<br/><br/>

                     We have reset your password and your new password is {new_password}<br/><br/>

                     You can now login using your login email and the new password from <a href="{login_url}">here</a>.
                 '''.format(new_password=new_password, login_url=settings.DOMAIN_URL + settings.LOGIN_URL)

        # send_mail(to_email, subject, text_message, html_message)
        Thread(target=send_mail, args=(to_email, subject, text_message, html_message)).start()

        response = UserStatusCodes.PASSWORD_CHANGED

        return Response(response, status=status.HTTP_200_OK)


class ChangePasswordAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # access_token = request.data['access_token']
        user = request.auth.user
        if not user:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        new_password = request.data.get('new_password', None)
        if not new_password:
            return Response(UserStatusCodes.NEW_PASSWORD_NOT_FOUND, status=status.HTTP_200_OK)

        user.set_password(new_password)
        user.save()

        return Response(UserStatusCodes.PASSWORD_CHANGED, status=status.HTTP_200_OK)


class ProfileDetailsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = get_loggedin_user(request)
        if not user:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        profile = UserProfile.objects.filter(user=user).first()
        if not profile:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        response = UserStatusCodes.PROFILE_DETAILS
        response['data'] = profile.to_dict()
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = get_loggedin_user(request)
        if not user:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        profile = UserProfile.objects.filter(user=user).first()
        if not profile:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        name = request.data.get('name', None)
        picture = request.FILES.get('picture', None)

        if name:
            profile.name = name
        if picture:
            profile.picture = picture
        profile.save()

        response = UserStatusCodes.PROFILE_UPDATED
        response['data'] = profile.to_dict()
        return Response(response, status=status.HTTP_200_OK)


class GetProfileDetailsAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = get_loggedin_user(request)
        if not user:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        profile = UserProfile.objects.filter(user=user).first()
        if not profile:
            return Response(UserStatusCodes.USER_NOT_FOUND, status=status.HTTP_200_OK)

        response = UserStatusCodes.PROFILE_DETAILS
        response['data'] = profile.to_dict()
        return Response(response, status=status.HTTP_200_OK)
