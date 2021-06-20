from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from .managers import UserManager
from django.utils import timezone

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
        return self.email


    def get_full_name(self):
        return self.first_name+self.last_name

#Abstract Class for Common fields in Post and comments
class CommonInfo(models.Model):
    body = models.TextField()
    author = models.ForeignKey('User',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract=True

    #common method for soft deleting data
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

#Post
class Post(CommonInfo):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


#Comments
class Comments(CommonInfo):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments',editable=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE,related_name='subcomments',null=True,blank=True)
    is_subcomment = models.BooleanField(default=False)

    def __str__(self):
        return self.body
