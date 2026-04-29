"""
URL routing for the shopping app.
Uses nested routes: /api/v1/lists/{list_pk}/items/
"""

from django.urls import path

from .views import ItemViewSet, ShoppingListViewSet

# Shopping list routes
list_list = ShoppingListViewSet.as_view({"get": "list", "post": "create"})
list_detail = ShoppingListViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)
list_complete = ShoppingListViewSet.as_view({"post": "complete"})

# Item routes (nested under a list)
item_list = ItemViewSet.as_view({"get": "list", "post": "create"})
item_detail = ItemViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)
item_toggle = ItemViewSet.as_view({"post": "toggle"})

urlpatterns = [
    # Lists
    path("lists/", list_list, name="shoppinglist-list"),
    path("lists/<int:pk>/", list_detail, name="shoppinglist-detail"),
    path("lists/<int:pk>/complete/", list_complete, name="shoppinglist-complete"),
    # Items (nested)
    path("lists/<int:list_pk>/items/", item_list, name="item-list"),
    path("lists/<int:list_pk>/items/<int:pk>/", item_detail, name="item-detail"),
    path("lists/<int:list_pk>/items/<int:pk>/toggle/", item_toggle, name="item-toggle"),
]
