from django.urls import path
from .views import product_list, product_detail, search_suggestions

urlpatterns = [
    path("", product_list, name="product_list"),
    path("api/search-suggestions/", search_suggestions, name="search_suggestions"),
    path("<slug:slug>/", product_detail, name="product_detail"),
]
