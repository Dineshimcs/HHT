import os
import sys
from pathlib import Path

# Add project root and apps directory to sys.path so imports work on Vercel
path = Path(__file__).resolve().parent.parent
sys.path.append(str(path))
sys.path.append(str(path / "apps"))

# Set Django settings module to production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

# Automatic static files collection check for Vercel Serverless environment
staticfiles_dir = path / "staticfiles"
if not staticfiles_dir.exists() or not any(staticfiles_dir.iterdir()):
    try:
        call_command('collectstatic', interactive=False, clear=True)
    except Exception as e:
        print(f"Auto collectstatic warning: {e}")

application = get_wsgi_application()

# Vercel serverless function entrypoint
app = application
