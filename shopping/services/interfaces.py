"""
Abstract service interfaces (Interface Segregation Principle).

Services orchestrate business logic and depend only on repository abstractions,
making them fully testable without a real database.
"""
from abc import ABC, abstractmethod


class AbstractShoppingListService(ABC):
    """Business-logic interface for shopping list operations."""

    @abstractmethod
    def get_all_lists(self):
        raise NotImplementedError

    @abstractmethod
    def get_list(self, list_id: int):
        raise NotImplementedError

    @abstractmethod
    def create_list(self, name: str, description: str = "") -> object:
        raise NotImplementedError

    @abstractmethod
    def update_list(self, list_id: int, **kwargs) -> object:
        raise NotImplementedError

    @abstractmethod
    def delete_list(self, list_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def complete_list(self, list_id: int) -> object:
        raise NotImplementedError


class AbstractItemService(ABC):
    """Business-logic interface for item operations."""

    @abstractmethod
    def get_items_for_list(self, list_id: int):
        raise NotImplementedError

    @abstractmethod
    def get_item(self, item_id: int):
        raise NotImplementedError

    @abstractmethod
    def add_item(self, list_id: int, name: str, quantity: int = 1, unit: str = "", notes: str = "") -> object:
        raise NotImplementedError

    @abstractmethod
    def update_item(self, item_id: int, **kwargs) -> object:
        raise NotImplementedError

    @abstractmethod
    def delete_item(self, item_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def toggle_item(self, item_id: int) -> object:
        raise NotImplementedError
