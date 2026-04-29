"""
Concrete service implementations.

Services contain all business rules and depend only on the repository
interfaces (Dependency Inversion Principle). This makes them fully
unit-testable with fake/mock repositories.
"""
from django.core.exceptions import ValidationError

from ..repositories.interfaces import AbstractItemRepository, AbstractShoppingListRepository
from .interfaces import AbstractItemService, AbstractShoppingListService


class ShoppingListService(AbstractShoppingListService):
    """Orchestrates shopping-list business logic."""

    def __init__(self, repository: AbstractShoppingListRepository) -> None:
        # Dependency injection — avoids hard-coupling to a concrete class
        self._repository = repository

    def get_all_lists(self):
        return self._repository.get_all()

    def get_list(self, list_id: int):
        return self._repository.get_by_id(list_id)

    def create_list(self, name: str, description: str = "") -> object:
        name = name.strip()
        if not name:
            raise ValidationError("The shopping list must have a name.")
        return self._repository.create(name=name, description=description)

    def update_list(self, list_id: int, **kwargs) -> object:
        if "name" in kwargs:
            kwargs["name"] = kwargs["name"].strip()
            if not kwargs["name"]:
                raise ValidationError("The shopping list must have a name.")
        return self._repository.update(list_id, **kwargs)

    def delete_list(self, list_id: int) -> None:
        self._repository.delete(list_id)

    def complete_list(self, list_id: int) -> object:
        return self._repository.update(list_id, is_completed=True)


class ItemService(AbstractItemService):
    """Orchestrates item business logic."""

    def __init__(
        self,
        item_repository: AbstractItemRepository,
        list_repository: AbstractShoppingListRepository,
    ) -> None:
        self._item_repository = item_repository
        self._list_repository = list_repository

    def get_items_for_list(self, list_id: int):
        # Ensure the list exists first (raises ObjectDoesNotExist if not)
        self._list_repository.get_by_id(list_id)
        return self._item_repository.get_by_list(list_id)

    def get_item(self, item_id: int):
        return self._item_repository.get_by_id(item_id)

    def add_item(self, list_id: int, name: str, quantity: int = 1, unit: str = "", notes: str = "") -> object:
        name = name.strip()
        if not name:
            raise ValidationError("Item must have a name.")
        if quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
        # Ensure parent list exists
        self._list_repository.get_by_id(list_id)
        return self._item_repository.create(
            list_id=list_id, name=name, quantity=quantity, unit=unit, notes=notes
        )

    def update_item(self, item_id: int, **kwargs) -> object:
        if "quantity" in kwargs and kwargs["quantity"] < 1:
            raise ValidationError("Quantity must be at least 1.")
        return self._item_repository.update(item_id, **kwargs)

    def delete_item(self, item_id: int) -> None:
        self._item_repository.delete(item_id)

    def toggle_item(self, item_id: int) -> object:
        return self._item_repository.toggle_check(item_id)
