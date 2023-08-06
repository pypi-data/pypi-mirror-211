from django.db import models


class Source(models.Model):
    source_url = models.URLField()  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore

    def __str__(self):
        return self.source_url


class BaseScraperModel(models.Model):
    class Meta:
        abstract = True

    url = models.URLField()  # type: ignore
    title = models.CharField(max_length=500)  # type: ignore
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore
    updated_at = models.DateTimeField(auto_now=True)  # type: ignore
    exists_in_source = models.BooleanField(default=True)  # type: ignore
    is_disabled = models.BooleanField(default=False)  # type: ignore
    disabled_reason = models.CharField(max_length=500, default='')  # type: ignore

    def __str__(self):
        return self.url


class BaseScrapeStatus(models.Model):
    class Meta:
        abstract = True
    # Override this for specific model
    # Could probably use GeneriForeignKey, but let's try this first
    # page_object = models.ForeignKey(BaseScraperModel, on_delete=models.CASCADE)
    status = models.IntegerField()  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore
