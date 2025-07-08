from django.contrib import admin
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

for model in [SocialAccount, SocialApp, SocialToken]:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

from .models import Anime, Episode, Category

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1

class AnimeAdmin(admin.ModelAdmin):
    inlines = [EpisodeInline]
    list_display = ['title', 'created_at']
    exclude = ['likes', 'views']  # Bu maydonlar admin formda ko‘rinmaydi
    # filter_horizontal = ('categories',)  # Agar kerak bo‘lsa, qo‘shing

admin.site.register(Anime, AnimeAdmin)
admin.site.register(Category)
