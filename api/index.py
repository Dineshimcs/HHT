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

application = get_wsgi_application()

# Vercel serverless function entrypoint
app = application
