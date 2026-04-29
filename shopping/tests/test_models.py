"""
TDD tests for shopping models.
Red → Green → Refactor.
"""

import pytest

from shopping.models import Item, ShoppingList

from .factories import ItemFactory, ShoppingListFactory


@pytest.mark.django_db
class TestShoppingListModel:
    """Tests for the ShoppingList model."""

    def test_create_shopping_list(self):
        """A ShoppingList can be saved to the database with required fields."""
        sl = ShoppingListFactory(name="Compra semanal")
        assert sl.pk is not None
        assert sl.name == "Compra semanal"
        assert sl.is_completed is False

    def test_str_representation(self):
        """__str__ returns the list name."""
        sl = ShoppingListFactory(name="Mi lista")
        assert str(sl) == "Mi lista"

    def test_mark_as_completed(self):
        """mark_as_completed sets is_completed=True and persists it."""
        sl = ShoppingListFactory(is_completed=False)
        sl.mark_as_completed()
        sl.refresh_from_db()
        assert sl.is_completed is True

    def test_total_items_empty_list(self):
        """total_items returns 0 for a new list with no items."""
        sl = ShoppingListFactory()
        assert sl.total_items() == 0

    def test_total_items_with_items(self):
        """total_items returns the correct count after adding items."""
        sl = ShoppingListFactory()
        ItemFactory.create_batch(3, shopping_list=sl)
        assert sl.total_items() == 3

    def test_checked_items(self):
        """checked_items returns only the items that are checked."""
        sl = ShoppingListFactory()
        ItemFactory.create_batch(2, shopping_list=sl, is_checked=True)
        ItemFactory.create_batch(3, shopping_list=sl, is_checked=False)
        assert sl.checked_items() == 2

    def test_ordering_newest_first(self):
        """ShoppingList default ordering is newest first."""
        sl1 = ShoppingListFactory(name="Primera")
        sl2 = ShoppingListFactory(name="Segunda")
        lists = list(ShoppingList.objects.all())
        assert lists[0] == sl2
        assert lists[1] == sl1


@pytest.mark.django_db
class TestItemModel:
    """Tests for the Item model."""

    def test_create_item(self):
        """An Item can be saved with required fields."""
        item = ItemFactory(name="Leche", quantity=2, unit="litros")
        assert item.pk is not None
        assert item.name == "Leche"

    def test_str_with_unit(self):
        """__str__ includes quantity and unit when unit is set."""
        item = ItemFactory(name="Leche", quantity=2, unit="litros")
        assert str(item) == "Leche (2 litros)"

    def test_str_without_unit(self):
        """__str__ shows name x quantity when unit is empty."""
        item = ItemFactory(name="Huevos", quantity=12, unit="")
        assert str(item) == "Huevos x12"

    def test_toggle_check_marks_checked(self):
        """toggle_check changes is_checked from False to True."""
        item = ItemFactory(is_checked=False)
        item.toggle_check()
        item.refresh_from_db()
        assert item.is_checked is True

    def test_toggle_check_unmarks_checked(self):
        """toggle_check changes is_checked from True to False."""
        item = ItemFactory(is_checked=True)
        item.toggle_check()
        item.refresh_from_db()
        assert item.is_checked is False

    def test_cascade_delete(self):
        """Deleting a ShoppingList also deletes its Items."""
        sl = ShoppingListFactory()
        ItemFactory.create_batch(3, shopping_list=sl)
        sl_id = sl.pk
        sl.delete()
        assert Item.objects.filter(shopping_list_id=sl_id).count() == 0
