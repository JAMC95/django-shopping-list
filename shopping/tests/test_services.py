"""
TDD unit tests for the service layer.
These tests use mock/stub repositories so NO database is required.
This demonstrates the power of the Dependency Inversion Principle.
"""
from unittest.mock import MagicMock, call

import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from shopping.services.shopping_service import ItemService, ShoppingListService


class FakeShoppingListRepository:
    """In-memory stub repository for unit testing services without DB."""

    def __init__(self, initial=None):
        self._store = {obj.id: obj for obj in (initial or [])}
        self._next_id = max((o.id for o in (initial or [])), default=0) + 1

    def _make_obj(self, **kwargs):
        obj = MagicMock()
        obj.id = self._next_id
        self._next_id += 1
        for k, v in kwargs.items():
            setattr(obj, k, v)
        return obj

    def get_all(self):
        return list(self._store.values())

    def get_by_id(self, list_id):
        if list_id not in self._store:
            raise ObjectDoesNotExist(f"ShoppingList {list_id} not found")
        return self._store[list_id]

    def create(self, name, description=""):
        obj = self._make_obj(name=name, description=description, is_completed=False)
        self._store[obj.id] = obj
        return obj

    def update(self, list_id, **kwargs):
        obj = self.get_by_id(list_id)
        for k, v in kwargs.items():
            setattr(obj, k, v)
        return obj

    def delete(self, list_id):
        self.get_by_id(list_id)
        del self._store[list_id]


class TestShoppingListService:
    """Pure unit tests — no database involved."""

    def setup_method(self):
        self.repo = FakeShoppingListRepository()
        self.service = ShoppingListService(self.repo)

    def test_create_list_valid_name(self):
        sl = self.service.create_list(name="  Verduras  ")
        assert sl.name == "Verduras"  # name is stripped

    def test_create_list_empty_name_raises(self):
        with pytest.raises(ValidationError):
            self.service.create_list(name="   ")

    def test_get_all_lists_empty(self):
        result = self.service.get_all_lists()
        assert result == []

    def test_get_all_lists_returns_all(self):
        self.service.create_list("Lista 1")
        self.service.create_list("Lista 2")
        assert len(self.service.get_all_lists()) == 2

    def test_delete_list_removes_it(self):
        sl = self.service.create_list("Eliminar")
        self.service.delete_list(sl.id)
        with pytest.raises(ObjectDoesNotExist):
            self.service.get_list(sl.id)

    def test_delete_nonexistent_raises(self):
        with pytest.raises(ObjectDoesNotExist):
            self.service.delete_list(9999)

    def test_complete_list_sets_flag(self):
        sl = self.service.create_list("Lista")
        completed = self.service.complete_list(sl.id)
        assert completed.is_completed is True

    def test_update_list_empty_name_raises(self):
        sl = self.service.create_list("Lista")
        with pytest.raises(ValidationError):
            self.service.update_list(sl.id, name="")


class FakeItemRepository:
    """In-memory stub item repository."""

    def __init__(self):
        self._store = {}
        self._next_id = 1

    def _make_item(self, **kwargs):
        obj = MagicMock()
        obj.id = self._next_id
        self._next_id += 1
        for k, v in kwargs.items():
            setattr(obj, k, v)
        obj.is_checked = False
        return obj

    def get_by_list(self, list_id):
        return [v for v in self._store.values() if v.shopping_list_id == list_id]

    def get_by_id(self, item_id):
        if item_id not in self._store:
            raise ObjectDoesNotExist(f"Item {item_id} not found")
        return self._store[item_id]

    def create(self, list_id, name, quantity=1, unit="", notes=""):
        obj = self._make_item(shopping_list_id=list_id, name=name, quantity=quantity, unit=unit, notes=notes)
        self._store[obj.id] = obj
        return obj

    def update(self, item_id, **kwargs):
        obj = self.get_by_id(item_id)
        for k, v in kwargs.items():
            setattr(obj, k, v)
        return obj

    def delete(self, item_id):
        self.get_by_id(item_id)
        del self._store[item_id]

    def toggle_check(self, item_id):
        obj = self.get_by_id(item_id)
        obj.is_checked = not obj.is_checked
        return obj


class TestItemService:
    def setup_method(self):
        self.list_repo = FakeShoppingListRepository()
        self.item_repo = FakeItemRepository()
        self.service = ItemService(self.item_repo, self.list_repo)
        # Create a list to add items to
        self.shopping_list = self.list_repo.create("Mi lista")

    def test_add_item_valid(self):
        item = self.service.add_item(self.shopping_list.id, "Manzanas", quantity=3, unit="kg")
        assert item.name == "Manzanas"
        assert item.quantity == 3

    def test_add_item_empty_name_raises(self):
        with pytest.raises(ValidationError):
            self.service.add_item(self.shopping_list.id, "  ")

    def test_add_item_zero_quantity_raises(self):
        with pytest.raises(ValidationError):
            self.service.add_item(self.shopping_list.id, "Pan", quantity=0)

    def test_add_item_to_nonexistent_list_raises(self):
        with pytest.raises(ObjectDoesNotExist):
            self.service.add_item(9999, "Pan")

    def test_toggle_item_flips_state(self):
        item = self.service.add_item(self.shopping_list.id, "Leche")
        assert item.is_checked is False
        toggled = self.service.toggle_item(item.id)
        assert toggled.is_checked is True

    def test_delete_item(self):
        item = self.service.add_item(self.shopping_list.id, "Queso")
        self.service.delete_item(item.id)
        with pytest.raises(ObjectDoesNotExist):
            self.service.get_item(item.id)

    def test_get_items_for_nonexistent_list_raises(self):
        with pytest.raises(ObjectDoesNotExist):
            self.service.get_items_for_list(9999)
