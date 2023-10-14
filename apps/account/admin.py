from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.http import HttpResponseRedirect

from apps.utils.mixins.admin.core import get_obj_link_field, ExportCsvMixin


@admin.register(get_user_model())
class UserAdmin(DjangoUserAdmin, ExportCsvMixin):
    list_display = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'pw_reset_on_login',
        'created_at',
        'modified_at',
    ]

    list_display_links = [
        'id',
    ]

    search_fields = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    ]

    fieldsets = (
        (
            None, {
                'fields': (
                    'id', 'email', 'username', 'password', 'last_login', 'created_at', 'modified_at',
                )
            }
        ),
        (
            'Personal info', {
                'fields': (
                    'first_name', 'last_name',
                )
            }
        ),
        (
            'Permissions', {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser', 'pw_reset_on_login', 'groups', 'user_permissions',
                )
            }
        ),
    )

    readonly_fields = [
        'id',
        'last_login',
        'created_at',
        'modified_at',
        'membership',
    ]

    change_form_template = "core/admin/account_user_change_form.html"

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'pw_reset_on_login',
        'groups',
    )

    ordering = ('email',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2',)
        }),
    )

    def newsletter(self, obj):
        return get_obj_link_field(obj.newsletter, 'newsletter')

    def membership(self, obj):
        return get_obj_link_field(obj.membership, 'membership')

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super().add_view(request)

    def response_change(self, request, obj):
        if 'add_newsletter_obj' in request.POST:
            obj.update_or_create_newsletter_obj()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return super().response_change(request, obj)
