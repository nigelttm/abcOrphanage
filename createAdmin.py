import os
import django

##append path accordingly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abcOrphanage.settings')
django.setup()

from abcApp.models import User

User.create_user(user_id='admin',password='admin', role='admin')