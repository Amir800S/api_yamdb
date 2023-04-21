from django.contrib import admin

from .models import User, Title, Genre, Category


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'bio',
    )
    list_filter = ('username',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)