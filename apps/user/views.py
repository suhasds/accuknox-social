from django.shortcuts import render
from django.views.generic import View
from main.settings import settings

from apps.user.auth import LoginRequired


class DashboardView(LoginRequired, View):

    def get(self, request, *args, **kwargs):
        # some logic
        context = {}
        return render(request, 'user_account/base.html', context)


class LoginView(View):

    def get(self, request, *args, **kwargs):
        context = {'google_client_id': settings.GOOGLE_CLIENT_ID}
        return render(request, 'user_account/login.html', context=context)


class SignupView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'user_account/signup.html')


class ForgotPasswordView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'user_account/forgot_password.html')


class UserEmailVerificationView(View):

    def get(self, request, *args, **kwargs):
        # lazy load
        from apps.user.models import UserProfile
        from apps.commons.status_codes import UserStatusCodes

        try:
            user_profile_id = self.kwargs.get('user_profile_id', None)
            user_profile = UserProfile.objects.filter(record_id=user_profile_id).first()
            if not user_profile:
                context = UserStatusCodes.EMAIL_VERIFICATION_FAILED
                context['email_verified'] = False
                return render(request, 'user_account/email_verification.html', context)

            user_profile.email_verified = True
            user_profile.save()
            context = UserStatusCodes.EMAIL_VERIFIED
            context['email_verified'] = True
            return render(request, 'user_account/email_verification.html', context)
        except Exception as e:
            context = UserStatusCodes.EMAIL_VERIFICATION_FAILED
            context['email_verified'] = False
            return render(request, 'user_account/email_verification.html', context)
