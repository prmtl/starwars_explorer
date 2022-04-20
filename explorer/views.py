from django.views.generic.list import ListView

from .models import Collection


# NOTE: this could be also paginated but there is no such requirement for now
class CollectionListView(ListView):
    model = Collection
