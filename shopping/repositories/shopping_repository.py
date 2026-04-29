"""
Django ORM implementations of the repository interfaces.

These are the concrete classes that actually talk to the database.
Swapping the database backend only requires a new implementation of the
abstract interface — no changes to services or views (Open/Closed Principle).
"""

from django.core.exceptions import ObjectDoesNotExist

from ..models import Item, ShoppingList
from .interfaces import AbstractItemRepository, AbstractShoppingListRepository


class DjangoShoppingListRepository(AbstractShoppingListRepository):
    """Concrete repository using Django ORM for ShoppingList."""

    def get_all(self):
        return ShoppingList.objects.all()

    def get_by_id(self, list_id: int) -> ShoppingList:
        try:
            return ShoppingList.objects.get(pk=list_id)
        except ShoppingList.DoesNotExist:
            raise ObjectDoesNotExist(f"ShoppingList with id={list_id} does not exist.")

    def create(self, name: str, description: str = "") -> ShoppingList:
        return ShoppingList.objects.create(name=name, description=description)

    def update(self, list_id: int, **kwargs) -> ShoppingList:
        shopping_list = self.get_by_id(list_id)
        allowed_fields = {"name", "description", "is_completed"}
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(shopping_list, field, value)
        shopping_list.save()
        return shopping_list

    def delete(self, list_id: int) -> None:
        shopping_list = self.get_by_id(list_id)
        shopping_list.delete()


class DjangoItemRepository(AbstractItemRepository):
    """Concrete repository using Django ORM for Item."""

    def get_by_list(self, list_id: int):
        return Item.objects.filter(shopping_list_id=list_id)

    def get_by_id(self, item_id: int) -> Item:
        try:
            return Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise ObjectDoesNotExist(f"Item with id={item_id} does not exist.")

    def create(
        self,
        list_id: int,
        name: str,
        quantity: int = 1,
        unit: str = "",
        notes: str = "",
    ) -> Item:
        return Item.objects.create(
            shopping_list_id=list_id,
            name=name,
            quantity=quantity,
            unit=unit,
            notes=notes,
        )

    def update(self, item_id: int, **kwargs) -> Item:
        item = self.get_by_id(item_id)
        allowed_fields = {"name", "quantity", "unit", "notes", "is_checked"}
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(item, field, value)
        item.save()
        return item

    def delete(self, item_id: int) -> None:
        item = self.get_by_id(item_id)
        item.delete()

    def toggle_check(self, item_id: int) -> Item:
        item = self.get_by_id(item_id)
        item.toggle_check()
        return item
