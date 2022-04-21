from django.urls import path

from .views import CollectionDetailView, CollectionFetchView, CollectionListView, CollectionValueCountView

urlpatterns = [
    path("", CollectionListView.as_view(), name="collection-list"),
    path("fetch/", CollectionFetchView.as_view(), name="collection-fetch"),
    path("<uuid:pk>/", CollectionDetailView.as_view(), name="collection-detail"),
    path("<uuid:pk>/value_count/", CollectionValueCountView.as_view(), name="collection-value-count"),
]
