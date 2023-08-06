from django.contrib import admin
from authentication_app.models import BlacklistToken
from authentication_app.models import OutstandingToken

from authentication_app.utils.userConfig import getPref

pref = getPref()


if pref['Outstanding_REQUIRED']:
    admin.site.register(OutstandingToken)
if pref['Blacklist_REQUIRED']:
    admin.site.register(BlacklistToken)
