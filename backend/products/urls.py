from django.urls import path
from .views import start_search, search_status

urlpatterns = [
    path("start-search/", start_search),
    path("search-status/<str:search_id>/", search_status),
]