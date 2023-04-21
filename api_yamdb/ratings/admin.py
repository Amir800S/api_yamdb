from django.contrib import admin

from ratings.models import Comment, Review

admin.site.register(Comment)
admin.site.register(Review)
