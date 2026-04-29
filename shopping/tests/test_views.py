"""
TDD integration tests for the API views.
Uses Django test client + real database (pytest-django).
"""
import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from shopping.models import Item, ShoppingList

from .factories import ItemFactory, ShoppingListFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestShoppingListAPI:
    BASE_URL = "/api/v1/lists/"

    def test_list_empty(self, api_client):
        response = api_client.get(self.BASE_URL)
        assert response.status_code == 200
        assert response.data == []

    def test_list_returns_all(self, api_client):
        ShoppingListFactory.create_batch(2)
        response = api_client.get(self.BASE_URL)
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_create_list_success(self, api_client):
        payload = {"name": "Frutas de temporada", "description": "Para la semana"}
        response = api_client.post(self.BASE_URL, data=payload, format="json")
        assert response.status_code == 201
        assert response.data["name"] == "Frutas de temporada"
        assert ShoppingList.objects.count() == 1

    def test_create_list_missing_name_fails(self, api_client):
        response = api_client.post(self.BASE_URL, data={}, format="json")
        assert response.status_code == 400

    def test_retrieve_list(self, api_client):
        sl = ShoppingListFactory(name="Test")
        response = api_client.get(f"{self.BASE_URL}{sl.pk}/")
        assert response.status_code == 200
        assert response.data["name"] == "Test"

    def test_retrieve_nonexistent_returns_404(self, api_client):
        response = api_client.get(f"{self.BASE_URL}99999/")
        assert response.status_code == 404

    def test_update_list(self, api_client):
        sl = ShoppingListFactory(name="Original")
        response = api_client.put(f"{self.BASE_URL}{sl.pk}/", data={"name": "Actualizada"}, format="json")
        assert response.status_code == 200
        assert response.data["name"] == "Actualizada"

    def test_delete_list(self, api_client):
        sl = ShoppingListFactory()
        response = api_client.delete(f"{self.BASE_URL}{sl.pk}/")
        assert response.status_code == 204
        assert ShoppingList.objects.count() == 0

    def test_complete_list(self, api_client):
        sl = ShoppingListFactory(is_completed=False)
        response = api_client.post(f"{self.BASE_URL}{sl.pk}/complete/")
        assert response.status_code == 200
        assert response.data["is_completed"] is True

    def test_response_includes_items_field(self, api_client):
        sl = ShoppingListFactory()
        ItemFactory.create_batch(2, shopping_list=sl)
        response = api_client.get(f"{self.BASE_URL}{sl.pk}/")
        assert "items" in response.data
        assert len(response.data["items"]) == 2

    def test_response_includes_totals(self, api_client):
        sl = ShoppingListFactory()
        ItemFactory.create_batch(3, shopping_list=sl)
        ItemFactory.create_batch(1, shopping_list=sl, is_checked=True)
        response = api_client.get(f"{self.BASE_URL}{sl.pk}/")
        assert response.data["total_items"] == 4
        assert response.data["checked_items"] == 1


@pytest.mark.django_db
class TestItemAPI:
    def _items_url(self, list_pk):
        return f"/api/v1/lists/{list_pk}/items/"

    def _item_url(self, list_pk, item_pk):
        return f"/api/v1/lists/{list_pk}/items/{item_pk}/"

    def test_list_items(self, api_client):
        sl = ShoppingListFactory()
        ItemFactory.create_batch(3, shopping_list=sl)
        response = api_client.get(self._items_url(sl.pk))
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_create_item(self, api_client):
        sl = ShoppingListFactory()
        payload = {"name": "Leche", "quantity": 2, "unit": "litros"}
        response = api_client.post(self._items_url(sl.pk), data=payload, format="json")
        assert response.status_code == 201
        assert response.data["name"] == "Leche"
        assert Item.objects.count() == 1

    def test_create_item_in_nonexistent_list_returns_400(self, api_client):
        payload = {"name": "Pan", "quantity": 1}
        response = api_client.post(self._items_url(99999), data=payload, format="json")
        assert response.status_code == 400

    def test_delete_item(self, api_client):
        sl = ShoppingListFactory()
        item = ItemFactory(shopping_list=sl)
        response = api_client.delete(self._item_url(sl.pk, item.pk))
        assert response.status_code == 204
        assert Item.objects.count() == 0

    def test_toggle_item(self, api_client):
        sl = ShoppingListFactory()
        item = ItemFactory(shopping_list=sl, is_checked=False)
        response = api_client.post(f"{self._item_url(sl.pk, item.pk)}toggle/")
        assert response.status_code == 200
        assert response.data["is_checked"] is True

    def test_update_item(self, api_client):
        sl = ShoppingListFactory()
        item = ItemFactory(shopping_list=sl, name="Pan", quantity=1)
        response = api_client.put(
            self._item_url(sl.pk, item.pk),
            data={"name": "Pan integral", "quantity": 2},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["name"] == "Pan integral"
