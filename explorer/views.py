import logging

from django import forms
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from explorer.models import Collection
from explorer.services import collections, processing

# NOTE: logging could be configured better in django settings (adjust levels and format)
logger = logging.getLogger(__name__)


# NOTE: this could be also paginated but there is no such requirement for now
class CollectionListView(ListView):
    model = Collection


class CollectionDetailView(DetailView):
    model = Collection

    PAGE_SIZE = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        limit = int(self.request.GET.get("limit", self.PAGE_SIZE))
        collection_data = collections.load_collection_data(self.object, limit=limit)

        context["people"] = collection_data
        context["next_limit"] = limit + self.PAGE_SIZE

        return context


class CollectionValueCountView(DetailView):
    model = Collection
    template_name_suffix = "_value_count"

    def get_form_class(self, table):
        header = table[0]
        choices = [(field, field) for field in header]

        class ValueCountForm(forms.Form):
            fields = forms.MultipleChoiceField(
                choices=choices, widget=forms.CheckboxSelectMultiple(), required=False
            )

        return ValueCountForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = collections.load_table(self.object)
        form = self.get_form_class(table)(self.request.GET)

        selected_fields = []
        if form.is_valid():
            selected_fields = form.cleaned_data["fields"]

        try:
            aggregation = processing.count_selected_fields_combinations_for_table(table, selected_fields)
        except ValueError:
            aggregation = []

        context["form"] = form
        context["fields"] = selected_fields
        context["aggregation"] = aggregation
        return context


class CollectionFetchView(RedirectView):
    permanent = False
    pattern_name = "collection-list"

    def get(self, request, *args, **kwargs):
        logger.info("Trigger new fetch request")
        collection = collections.fetch_and_save_new_collection()
        logger.info("Fetched new collection %s to %s", collection, collection.file.path)
        return super().get(request, *args, **kwargs)
