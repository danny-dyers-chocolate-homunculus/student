from django.contrib import admin
from models import *
from core.models import User
from django.db import models

admin.site.register(User)


for model in models.get_models():
    try:
        admin.site.register(model)
    except Exception:
        continue