# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
#
# application = get_wsgi_application()

import os

from dj_static import Cling
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

application = Cling(get_wsgi_application())
