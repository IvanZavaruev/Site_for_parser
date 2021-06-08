from django.contrib import admin

from .models import Author, Years, Publication

admin.site.register(Author)
admin.site.register(Years)
admin.site.register(Publication)
