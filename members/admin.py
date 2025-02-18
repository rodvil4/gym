from django.contrib import admin

from django.contrib import admin
from .models import Member,Instructor,Tclass,Grupo

admin.site.register(Member)

admin.site.register(Instructor)

admin.site.register(Tclass)

admin.site.register(Grupo)
