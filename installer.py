info = {
    "title": "ODK Connector",
    "description": "ODK Connector app allows you to create a features service for your survey and make the data available to use with GeoNode",
    "author": 'Cartologic',
    "home_page":'',
    "help_url":"",
    "tags": ['Data Collection'],
    "licence":'BSD',
    "author_website": "http://www.cartologic.com",
    "single_instance": True
}

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
def install():
    pass

def uninstall():
    ContentType.objects.filter(app_label="odk").delete();