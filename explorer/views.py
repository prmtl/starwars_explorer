import logging

from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from explorer.models import Collection
from explorer.services import collections

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


class CollectionFetchView(RedirectView):
    permanent = False
    pattern_name = "collection-list"

    def get(self, request, *args, **kwargs):
        logger.info("Trigger new fetch request")
        collection = collections.fetch_and_save_new_collection()
        logger.info("Fetched new collection %s to %s", collection, collection.file.path)
        return super().get(request, *args, **kwargs)
