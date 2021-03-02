from django.contrib.auth.backends import ModelBackend

from remusgold.account.models import AdvUser


class EmailModelBackend(ModelBackend):
    """
    authentication class to login with the email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):

        if '@' in username:
            kwargs = {'email': username}
        else:
            return None
        if password is None:
            return None
        try:
            user = AdvUser.objects.get(**kwargs)

        except AdvUser.DoesNotExist:
            AdvUser.set_password(password)

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
