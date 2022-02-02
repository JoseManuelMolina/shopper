from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class CaseIntensitiveModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return super().authenticate(request, **kwargs)()

class EmailOrUsernameModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        auth_type = settings.AUTH_AUTHENTICATION_TYPE
        if auth_type == 'username':
            return super().authenticate(username, password)
        user_model = get_user_model()
        try:
            if auth_type == 'both':
                user = user_model.objects.get(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
            else:
                user = user_model.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None