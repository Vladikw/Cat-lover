from django.db import models


class User(models.Model):
    login = models.CharField(max_length=128, blank=False, null=False)
    password = models.CharField(max_length=24, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    name = models.CharField(max_length=128, blank=False, null=False)
    address = models.CharField(max_length=128, blank=True, null=True,
                               default=None)
    telephone = models.CharField(max_length=128, blank=True, null=True,
                                 default=None)
    is_blocked = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    removed = models.BooleanField(default=False)


class UserPhoto(models.Model):
    user = models.ForeignKey(User, blank=False, null=False,
                             on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users_photos/')
    status = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class Right(models.Model):
    name = models.CharField(max_length=16, blank=False, null=False)
    default_state = models.BooleanField(default=False)


class UserRight(models.Model):
    id_right = models.ForeignKey(Right, blank=False, null=False,
                                 on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, blank=False, null=False,
                                on_delete=models.CASCADE)
    actual_state = models.BooleanField(default=True)
