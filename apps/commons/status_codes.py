# Common Status Codes
from typing import Dict, Union


class CommonStatusCodes:
    SERVER_EXCEPTION = {
        'code': 500, 'reason': 'Internal Server exception, please find exception details for more info'
    }


# App auth status codes
class AppAuthStatusCodes:
    USER_FOUND = {
        'code': 200, 'reason': 'User found and token generated'
    }
    USER_NOT_FOUND = {
        'code': 1002, 'reason': 'User not found due to incorrect user name or password'
    }
    INCORRECT_CREDS = {
        'code': 1003, 'reason': 'Incorrect email/password. Please register if not an existing user!'
    }
    MISSING_FIELDS_FOR_LOGIN = {
        'code': 1004, 'reason': 'Either user name or password is missing'
    }
    MISSING_FIELDS_FOR_RESET = {
        'code': 1005, 'reason': 'Email is missing'
    }
    LOGIN_FAILED = {
        'code': 1006, 'reason': 'Error, Unable to login!'
    }


# customer status codes
class UserStatusCodes:
    REGISTRATION_SUCCESS = {
        'code': 200, 'reason': 'Registration was successful, please verify your email to login'
    }
    USER_LOGGED_OUT = {
        'code': 200, 'reason': 'User logged out successfully'
    }
    PASSWORD_CHANGED = {
        'code': 200, 'reason': 'Password changed successfully'
    }
    PROFILE_DETAILS = {
        'code': 200, 'reason': 'Profile details found'
    }
    EMAIL_VERIFICATION_LINK_SENT = {
        'code': 200, 'reason': 'Verification email successfully sent'
    }
    REGISTRATION_FAILED = {
        'code': 2002, 'reason': 'Registration was failed'
    }
    MISSING_FIELDS_FOR_REGISTRATION = {
        'code': 2003, 'reason': 'Missing mandatory fields for registration'
    }
    INVALID_USER_GROUP = {
        'code': 2004, 'reason': 'Missing mandatory fields for registration'
    }
    SAME_USER_EXISTS = {
        'code': 2005, 'reason': 'User already exists'
    }
    LOGIN_FAILED = {
        'code': 2006, 'reason': 'Login failed'
    }
    USER_NOT_FOUND = {
        'code': 2007, 'reason': 'User not found'
    }
    NEW_PASSWORD_NOT_FOUND = {
        'code': 2008, 'reason': 'New password not found'
    }
    EMAIL_NOT_VERIFIED = {
        'code': 2009, 'reason': 'Email not verified, please verify your email.'
    }
    EMAIL_VERIFIED = {
        'code': 200, 'reason': 'Email verified successfully.'
    }
    EMAIL_VERIFICATION_FAILED = {
        'code': 2010, 'reason': 'Error, Email verification failed.'
    }
    INVALID_EMAIL = {
        'code': 2011, 'reason': 'Invalid email format'
    }
