"""
TDD tests for the repository layer.
Testing concrete Django ORM repositories with real DB (pytest-django).
"""
import pytest
from django.core.exceptions import ObjectDoesNotExist

from shopping.repositories.shopping_repository import DjangoItemRepository, DjangoShoppingListRepository

from .factories import ItemFactory, ShoppingListFactory


@pytest.mark.django_db
class TestDjangoShoppingListRepository:
    def setup_method(self):
        self.repo = DjangoShoppingListRepository()

    def test_create_returns_shopping_list(self):
        sl = self.repo.create(name="Frutas")
        assert sl.pk is not None
        assert sl.name == "Frutas"

    def test_get_all_returns_queryset(self):
        ShoppingListFactory.create_batch(3)
        result = list(self.repo.get_all())
        assert len(result) == 3

    def test_get_by_id_returns_correct_list(self):
        sl = ShoppingListFactory(name="Lácteos")
        found = self.repo.get_by_id(sl.pk)
        assert found.pk == sl.pk

    def test_get_by_id_raises_for_missing(self):
        with pytest.raises(ObjectDoesNotExist):
            self.repo.get_by_id(99999)

    def test_update_changes_name(self):
        sl = ShoppingListFactory(name="Original")
        updated = self.repo.update(sl.pk, name="Actualizado")
        assert updated.name == "Actualizado"

    def test_delete_removes_record(self):
        sl = ShoppingListFactory()
        pk = sl.pk
        self.repo.delete(pk)
        with pytest.raises(ObjectDoesNotExist):
            self.repo.get_by_id(pk)


@pytest.mark.django_db
class TestDjangoItemRepository:
    def setup_method(self):
        self.repo = DjangoItemRepository()

    def test_create_returns_item(self):
        sl = ShoppingListFactory()
        item = self.repo.create(list_id=sl.pk, name="Pan", quantity=1)
        assert item.pk is not None
        assert item.name == "Pan"

    def test_get_by_list_returns_only_list_items(self):
        sl1 = ShoppingListFactory()
        sl2 = ShoppingListFactory()
        ItemFactory.create_batch(2, shopping_list=sl1)
        ItemFactory.create_batch(3, shopping_list=sl2)
        result = list(self.repo.get_by_list(sl1.pk))
        assert len(result) == 2

    def test_toggle_check_flips_state(self):
        item = ItemFactory(is_checked=False)
        toggled = self.repo.toggle_check(item.pk)
        assert toggled.is_checked is True

    def test_delete_removes_item(self):
        item = ItemFactory()
        pk = item.pk
        self.repo.delete(pk)
        with pytest.raises(ObjectDoesNotExist):
            self.repo.get_by_id(pk)
