from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Collection


# NOTE: this could be also paginated but there is no such requirement for now
class CollectionListView(ListView):
    model = Collection


class CollectionDetailView(DetailView):
    model = Collection


class CollectionFetchView(RedirectView):
    permanent = False
    pattern_name = "collection-list"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
