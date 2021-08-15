from django.contrib import admin

from .models import *

admin.site.register(Contact)
admin.site.register(ContactPoint)
admin.site.register(ContactPointMethod)
admin.site.register(ContactTag)
admin.site.register(UserWrapper)
