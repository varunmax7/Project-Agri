import os
from django.core.wsgi import get_wsgi_application

# Force overwrite the env var in case it was misspelled as 'onfig' in Vercel dashboard
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.prod'
application = get_wsgi_application()

# Required by Vercel's @vercel/python builder
app = application
