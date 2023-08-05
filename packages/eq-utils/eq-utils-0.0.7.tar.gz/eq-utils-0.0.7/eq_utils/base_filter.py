from django.urls import reverse
from admin_auto_filters.filters import AutocompleteFilter


class EqAutofilter(AutocompleteFilter):
    @staticmethod
    def get_queryset_for_field(model, name):
        return model.objects.get_queryset()

    def get_autocomplete_url(self, request, model_admin):
        '''
            Hook to specify your custom view for autocomplete,
            instead of default django admin's search_results.
        '''
        url_name = '%s:%s_%s_autocomplete'
        return reverse(url_name % (
            model_admin.admin_site.name, self.rel_model._meta.app_label,
            self.rel_model._meta.model_name))
