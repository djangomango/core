from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.log.modelmixins import ActionLogMixin


class AttentionStatusMixin(ActionLogMixin, models.Model):
    attention = models.BooleanField(_('Attention?'), default=False)
    attention_at = models.DateTimeField(_('Attention at'), blank=True, null=True)

    class Meta:
        abstract = True

    def add_attention(self, save=True):
        self.attention = True
        self.attention_at = timezone.now()

        if save:
            self.save(**{
                'action_tag': 'add_attention'
            })

    def remove_attention(self, save=True):
        self.attention = False
        self.attention_at = None

        if save:
            self.save(**{
                'action_tag': 'remove_attention'
            })


class RequestedStatusMixin(ActionLogMixin, models.Model):
    requested = models.BooleanField(_('Requested?'), default=False)
    requested_at = models.DateTimeField(_('Requested at'), blank=True, null=True)

    class Meta:
        abstract = True

    def add_requested(self, save=True):
        self.requested = True
        self.requested_at = timezone.now()

        if save:
            self.save(**{
                'action_tag': 'add_requested'
            })

    def remove_requested(self, save=True):
        self.requested = False
        self.requested_at = None

        if save:
            self.save(**{
                'action_tag': 'remove_requested'
            })


class ApprovedStatusMixin(ActionLogMixin, models.Model):
    approved = models.BooleanField(_('Approved?'), default=False)
    approved_at = models.DateTimeField(_('Approved at'), blank=True, null=True)
    denied_at = models.DateTimeField(_('Denied at'), blank=True, null=True)

    class Meta:
        abstract = True

    def add_approved(self, save=True):
        self.approved = True
        self.approved_at = timezone.now()

        if save:
            self.save(**{
                'action_tag': 'add_approved'
            })

    def remove_approved(self, save=True):
        self.approved = False
        self.approved_at = None

        if save:
            self.save(**{
                'action_tag': 'remove_approved'
            })

    def add_denied(self, save=True):
        self.approved = False
        self.denied_at = timezone.now()

        if save:
            self.save(**{
                'action_tag': 'add_denied'
            })

    def remove_denied(self, save=True):
        self.approved = True
        self.denied_at = None

        if save:
            self.save(**{
                'action_tag': 'remove_denied'
            })


class LifecycleRequestStatusMixin(AttentionStatusMixin, RequestedStatusMixin, ApprovedStatusMixin, models.Model):
    class Meta:
        abstract = True
