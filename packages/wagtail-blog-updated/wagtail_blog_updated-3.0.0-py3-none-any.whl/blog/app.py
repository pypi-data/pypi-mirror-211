
from django import apps as django_apps


class BlogConfig(django_apps.AppConfig):
    name = 'blog'
    verbose_name = 'Wagtail Blog'
    default_auto_field = 'django.db.models.AutoField'
