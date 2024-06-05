from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from apps.commons.models import BaseClass
from main.settings.settings import ENVIRONMENT
from django.core.validators import RegexValidator


class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=email)
        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseClass):
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(help_text='If the user an application admin', default=False)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    ALREADY_EXISTS = 'The user already exists'

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def has_perms(self, *args, **kwargs):
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def to_dict(self):
        return {
            'email': self.email,
            'is_active': self.is_active,
        }

    class Meta(BaseClass.Meta):
        db_table = 'user'


class UserProfile(BaseClass, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=256, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    #                              message="Phone number must be entered in the format: '+999999999'.")
    # phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    # phone_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['name']

    def to_dict(self):
        return {
            'id': str(self.record_id),
            'name': self.name,
            'email': self.user.email,
            'email_verified': self.email_verified,
            # 'phone': self.phone,
            # 'phone_verified': self.phone_verified,
            # 'user_groups': [grp for grp in self.user.groups.values_list('name', flat=True)],
            # 'user_permissions': get_user_permissions(self.end_user),
            # 'environment': ENVIRONMENT,
        }

    class Meta(BaseClass.Meta):
        db_table = 'user_profile'
