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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreInline(admin.TabularInline):
    model = Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'year',
                    'description')
    search_fields = ('name',)
    list_filter = ('name')
    list_editable = ('name', 'year',)
    empty_value_display = '-пусто-'
    list_editable = ('category',)
    inlines = [
        GenreInline
    ]

    def output_of_genres(self, obj):
        return ', '.join([str(genre) for genre in obj.genre.all()])


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
