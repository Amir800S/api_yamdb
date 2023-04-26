from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Category, Comment, Genre, Review, Title, User


class UserAdmin(BaseUserAdmin):
    """Админка юзера."""
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'bio',
    )
    list_display_links = (
        'username',
        'email',
    )
    list_editable = ('role', )
    list_filter = ('username', )
    search_fields = ('username', )
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """Админка коммента."""
    list_display = (
        'review',
        'author',
        'text',
        'pub_date',
    )
    list_filter = ('review',)
    search_fields = ('text',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    """Админка для ревью."""
    list_display = (
        'title',
        'author',
        'text',
        'score',
        'pub_date',
    )
    list_filter = ('title',)
    search_fields = ('text',)


class CategoryAdmin(admin.ModelAdmin):
    """Админка для категории."""
    list_display = ('pk',
                    'name',
                    'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    """Админка для жанра."""
    list_display = ('pk',
                    'name',
                    'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreInline(admin.TabularInline):
    model = Genre


class TitleAdmin(admin.ModelAdmin):
    """Админка для произведения."""
    list_display = ('pk',
                    'name',
                    'year',
                    'description')
    search_fields = ('name',)
    list_filter = ('name', )
    empty_value_display = '-пусто-'
    list_editable = ('category',)
    inlines = [
        GenreInline
    ]

    def output_of_genres(self, obj):
        return ', '.join([str(genre) for genre in obj.genre.all()])


admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
