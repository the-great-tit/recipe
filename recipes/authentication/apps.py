"""App config."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthConfig(AppConfig):
    """Register user app."""

    name = 'recipes.authentication'
    verbose_name = _('profiles')

    def ready(self):
        """Register a signal."""
        import recipes.authentication.signals  # noqa
