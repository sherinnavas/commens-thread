from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

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

#custom User class
class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True,null=True)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=100)
    is_staff = models.BooleanField(

            default=False,

        )
    is_active = models.BooleanField(

        default=True,

    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.username


    def get_full_name(self):
        return self.first_name+self.last_name

#Abstract Class for Common fields in Post and comments
class CommonInfo(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey('User',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract=True


#Post
class Post(CommonInfo):

    def __str__(self):
        return self.title


#Comments
class Comments(CommonInfo):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')


    def __str__(self):
        return self.title
