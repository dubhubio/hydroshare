"""
Copy the contents of this file to a new file local_settings.py
Values here will serve as overrides when developing locally
local_settings.py will not be version controlled so storing keys is acceptable
"""

import os
from kombu import Queue, Exchange

DEBUG = True
DISABLE_TASK_EMAILS = True

# Make these unique, and don't share it with anybody
SECRET_KEY = \
    "9e2e3c2d-8282-41b2-a027-de304c0bc3d944963c9a-4778-43e0-947c-38889e976dcab9f328cb-1576-4314-bfa6-70c42a6e773c"
NEVERCACHE_KEY = \
    "7b205669-41dd-40db-9b96-c6f93b66123496a56be1-607f-4dbf-bf62-3315fb353ce6f12a7d28-06ad-4ef7-9266-b5ea66ed2519"

ALLOWED_HOSTS = ['*']

# for Django/Mezzanine comments and ratings to require user login
COMMENTS_ACCOUNT_REQUIRED = True
RATINGS_ACCOUNT_REQUIRED = True
COMMENTS_USE_RATINGS = True

RABBITMQ_HOST = os.environ.get('RABBITMQ_PORT_5672_TCP_ADDR', 'localhost')
RABBITMQ_PORT = '5672'

POSTGIS_HOST = os.environ.get('POSTGIS_PORT_5432_TCP_ADDR', 'localhost')
POSTGIS_PORT = 5432
POSTGIS_DB = os.environ.get('POSTGIS_DB', 'postgres')
POSTGIS_PASSWORD = os.environ.get('POSTGIS_PASSWORD', 'postgres')
POSTGIS_USER = os.environ.get('POSTGIS_USER', 'postgres')

IPYTHON_SETTINGS = []
IPYTHON_BASE = '/hydroshare/static/media/ipython-notebook'
IPYTHON_HOST = '127.0.0.1'

# Celery settings
# customizations: we need a special queue for broadcast signals to all docker daemons.
# we also need a special queue for direct messages to all docker daemons.
BROKER_URL = 'amqp://guest:guest@{RABBITMQ_HOST}:{RABBITMQ_PORT}//'.format(RABBITMQ_HOST=RABBITMQ_HOST,
                                                                           RABBITMQ_PORT=RABBITMQ_PORT)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DEFAULT_QUEUE = 'default'
DEFAULT_EXCHANGE = Exchange('default', type='topic')

CELERY_QUEUES = (
    Queue('default', DEFAULT_EXCHANGE, routing_key='task.default'),
)
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'
CELERY_ROUTES = ('hs_core.router.HSTaskRouter',)

DISABLE_PERIODIC_TASKS = False

# Docker settings
DOCKER_URL = 'unix://docker.sock/'
DOCKER_API_VERSION = '1.12'

# CartoCSS settings
CARTO_HOME = '/hs_tmp/node_modules/carto'

USE_SOUTH = False
SITE_TITLE = "CUAHSI HydroShare"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        # DB name or path to database file if using sqlite3.
        "NAME": POSTGIS_DB,
        # Not used with sqlite3.
        "USER": POSTGIS_USER,
        # Not used with sqlite3.
        "PASSWORD": POSTGIS_PASSWORD,
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": POSTGIS_HOST,
        # Set to empty string for default. Not used with sqlite3.
        "PORT": POSTGIS_PORT,
    }
}
POSTGIS_VERSION = (2, 1, 1)

SHARED_NEG_KEY = 'hydroshareZonehydroshareuserZone'

# Native Docker iRODS developer local
USE_IRODS = True
IRODS_ROOT = '/tmp'
IRODS_ICOMMANDS_PATH = '/usr/bin'
IRODS_HOST = 'data.local.org'
IRODS_PORT = '1247'
IRODS_DEFAULT_RESOURCE = 'hydroshareReplResc'
IRODS_HOME_COLLECTION = '/hydroshareZone/home/wwwHydroProxy'
IRODS_CWD = '/hydroshareZone/home/wwwHydroProxy'
IRODS_ZONE = 'hydroshareZone'
IRODS_USERNAME = 'wwwHydroProxy'
IRODS_AUTH = 'wwwHydroProxy'
IRODS_GLOBAL_SESSION = True

# Remote user zone iRODS configuration
REMOTE_USE_IRODS = True

# iRODS customized bagit rule path
IRODS_BAGIT_RULE = 'hydroshare/irods/ruleGenerateBagIt_HS.r'
IRODS_BAGIT_PATH = 'bags'
IRODS_BAGIT_POSTFIX = 'zip'

IRODS_SERVICE_ACCOUNT_USERNAME = ''

HS_BAGIT_README_FILE_WITH_PATH = 'docs/bagit/readme.txt'

# crossref login credential for resource publication
USE_CROSSREF_TEST = True
CROSSREF_LOGIN_ID = ''
CROSSREF_LOGIN_PWD = ''

# Since Hyrax server on-demand update is only needed when private netCDF resources on www
# are made public, in local development environments or VM deployments other than the www
# production, this should not be run by setting RUN_HYRAX_UPDATE to False. RUN_HYRAX_UPDATE
# should only be set to True on www.hydroshare.org
RUN_HYRAX_UPDATE = False
HYRAX_SSH_HOST = ''
HYRAX_SSH_PROXY_USER = ''
HYRAX_SSH_PROXY_USER_PWD = ''
HYRAX_SCRIPT_RUN_COMMAND = ''

# hsuserproxy system user configuration used to create hydroshare iRODS users on-demand
HS_USER_ZONE_HOST = 'users.local.org'
LINUX_ADMIN_USER_FOR_HS_USER_ZONE = 'hsuserproxy'
LINUX_ADMIN_USER_PWD_FOR_HS_USER_ZONE = 'hsuserproxy'
LINUX_ADMIN_USER_CREATE_USER_IN_USER_ZONE_CMD = '/home/hsuserproxy/create_user.sh'
LINUX_ADMIN_USER_DELETE_USER_IN_USER_ZONE_CMD = '/home/hsuserproxy/delete_user.sh'

# HydroShare iRODS proxy user in the federated user zone
HS_IRODS_PROXY_USER_IN_USER_ZONE = 'localHydroProxy'
# HydroShare iRODS default storage resource in the federated user zone
HS_IRODS_USER_ZONE_DEF_RES = 'hydroshareLocalResc'
# HydroShare iRODS federated user zone name
HS_USER_IRODS_ZONE = 'hydroshareuserZone'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_HOST = ''
# EMAIL_PORT = ''
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = ''
# DEFAULT_SUPPORT_EMAIL=''

HYDROSHARE_SHARED_TEMP = '/shared_tmp'

# used by the mailchimp subscription job in hs_core/tasks.py
MAILCHIMP_ACTIVE_SUBSCRIBERS = "e210a70864"
MAILCHIMP_SUBSCRIBERS = "f0c27254e3"

# sendfile support for large files
# These must match settings in nginx
SENDFILE_ON = True
IRODS_USER_URI = "/irods-user"
IRODS_DATA_URI = "/irods-data"
LOCAL_CACHE_URI = "/local-cache"

# Needed for deployments to non-dev environments
RECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

# Insert a google maps key here when in production
# On local device google maps will show error in resource view since API key is blank here
MAPS_KEY = ''

# Uncomment the following code if you want to suppress some warnings on a local laptop
# TIME_ZONE = 'Etc/UTC'
# USE_TZ = False

"""
Silence ForeignKey Warnings:
hs_tracking.Visitor.user:(fields.W342) Setting unique=True on a ForeignKey has the same effect as using a OneToOneField.
hydroshare | HINT: ForeignKey(unique=True) is usually better served by a OneToOneField.
hydroshare | security.PasswordExpiry.user: (fields.W342) Setting unique=True on a ForeignKey has the same effect as
using a OneToOneField.
"""
# SILENCED_SYSTEM_CHECKS = ["mezzanine.core.W03", "fields.W342"]
