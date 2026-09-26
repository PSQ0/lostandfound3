
from django.urls import path
from core.views import (
    create_item,
    list_items,
    my_items,
    item_detail,
    update_item,
    delete_item,
)


urlpatterns = [
    path("", list_items, name="list_item"),
    path("my-items/", my_items, name="my_items"),
    path("create/", create_item, name="create_item"),
    path("<int:pk>/", item_detail, name='item_detail'),
    path("<int:pk>/edit/", update_item, name="update_item"),
    path("<int:pk>/delete/", delete_item, name="delete_item"),
]
