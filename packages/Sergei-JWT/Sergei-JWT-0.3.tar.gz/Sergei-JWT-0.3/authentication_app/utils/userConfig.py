from Sergei import settings


try:
    Outstanding_REQUIRED = False
    Outstanding_REQUIRED = settings.SERGEI['DATA_STORE']['POSTGRESQL']['OutstandingToken']
except KeyError:
    pass

try:
    Blacklist_REQUIRED = False
    Blacklist_REQUIRED = settings.SERGEI['DATA_STORE']['POSTGRESQL']['BlacklistToken']
except KeyError:
    pass

try:
    USE_REDIS = False
    USE_REDIS = settings.SERGEI['DATA_STORE']['REDIS']['REQUIRED']
except KeyError:
    pass


def getPref():
    """
     Helper function to resolve userpreference for outstanding and blacklist schema generation from settings files
     returns -> Outstanding_REQUIRED, Blacklist_REQUIRED
     """
    pref = dict()
    pref['Outstanding_REQUIRED'] = Outstanding_REQUIRED
    pref['Blacklist_REQUIRED'] = Blacklist_REQUIRED
    pref['USE_REDIS'] = USE_REDIS
    return pref
