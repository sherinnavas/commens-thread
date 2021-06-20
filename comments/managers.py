from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

#User Manager for overriding default unique username and enable unique email instead
class UserManager(BaseUserManager):

    def create_user(self, email, password=None,**kwargs):
        if email is None:
            raise TypeError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
