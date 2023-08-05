from django.contrib import admin
from django.conf import settings


class AdminHide(admin.ModelAdmin):
    """
        Este admin permite ocultar un modulo aun estando registrado.
    """

    def has_module_permission(self, request):
        if not settings.DEBUG:
            return False
        return request.user.has_module_perms(self.opts.app_label)


class EditOnlyTabularInline(admin.TabularInline):

    """
        Tabular inline sin permisos de creacion o borrado.
    """

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BaseReadOnlyAdmin(admin.ModelAdmin):

    """
        Admin de solo lectura.
    """

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
