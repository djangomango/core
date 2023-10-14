from solo.models import SingletonModel

from apps.utils.mixins.models.atoms import TimestampMixin
from apps.utils.mixins.models.components import PageMixin


class LandingPage(TimestampMixin, PageMixin, SingletonModel):

    class Meta:
        verbose_name = "Landing Page"
        verbose_name_plural = "Landing Page"

    def __str__(self):
        return "Landing page"
