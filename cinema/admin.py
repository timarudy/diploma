from django.contrib import admin
from .models import *

admin.site.register(MyUser)
admin.site.register(Cinema)
admin.site.register(Session)
admin.site.register(Purchase)
