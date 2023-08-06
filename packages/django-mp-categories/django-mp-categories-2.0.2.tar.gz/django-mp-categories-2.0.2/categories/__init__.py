
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


def setup_settings(settings, is_prod, **kwargs):

    if 'mptt' not in settings['INSTALLED_APPS']:
        settings['INSTALLED_APPS'] += ['mptt']


class CategoriesAppConfig(AppConfig):

    name = 'categories'
    verbose_name = _('Categories')


default_app_config = 'categories.CategoriesAppConfig'
