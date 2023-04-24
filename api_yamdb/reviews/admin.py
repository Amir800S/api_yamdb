from django.contrib import admin

from .models import User, Title, Genre, Category, Comment, Review


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


class CommentAdmin(admin.ModelAdmin):
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


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'year',
                    'description')
    search_fields = ('name',)
    list_filter = ('name', )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
