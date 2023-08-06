from django.db import models
from django.contrib.auth import get_user_model

from authentication_app.utils.userConfig import getPref

pref = getPref()


class BlacklistToken(models.Model):
    class Meta:
        managed = pref['Blacklist_REQUIRED']

    uuid = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=400, unique=True)
    Timestamp = models.DateTimeField(auto_now_add=True)


class OutstandingToken(models.Model):
    class Meta:
        managed = pref['Outstanding_REQUIRED']

    uuid = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=400, unique=True)
    Timestamp = models.DateTimeField(auto_now_add=True)
