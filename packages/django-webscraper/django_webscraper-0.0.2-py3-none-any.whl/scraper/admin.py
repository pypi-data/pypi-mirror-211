from django.contrib import admin

from scraper.models import BaseScrapeStatus, Source


class ScrapeStatusAdmin(admin.ModelAdmin):
    list_display = ['pk', 'page_object', 'status', 'created_at']


admin.site.register(BaseScrapeStatus.__subclasses__(), ScrapeStatusAdmin)


@admin.register(Source)
class ScrapeSourceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'source_url', 'created_at']
