import os
import sys

# Ensure the project root is in the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Force overwrite the env var in case it was misspelled as 'onfig' in Vercel dashboard
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.prod'

from config.wsgi import application
app = application
