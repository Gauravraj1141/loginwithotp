from .models import CustomUser

from django.contrib.auth.backends import ModelBackend


class OTPAuthBackend(ModelBackend):
    def authenticate(self, request, otp=None, **kwargs):
        try:
            # Try to find a user with a matching OTP
            user = CustomUser.objects.get(otp=otp)
        except CustomUser.DoesNotExist:
            # No user with a matching OTP was found
            return None

        # The OTP is valid, return the user object
        return user

    def get_user(self, user_id):
        try:
            # Try to get the user by ID
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            # No user with the given ID was found
            return None
