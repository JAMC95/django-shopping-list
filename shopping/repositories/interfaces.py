"""
Abstract interfaces for the repository layer (Dependency Inversion Principle).

By depending on abstractions, services can be tested with mock repositories
without touching the database.
"""
from abc import ABC, abstractmethod
from typing import List, Optional


class AbstractShoppingListRepository(ABC):
    """Interface for shopping list persistence operations."""

    @abstractmethod
    def get_all(self):
        """Return all shopping lists."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, list_id: int):
        """Return a single shopping list by primary key."""
        raise NotImplementedError

    @abstractmethod
    def create(self, name: str, description: str = "") -> object:
        """Persist a new shopping list and return it."""
        raise NotImplementedError

    @abstractmethod
    def update(self, list_id: int, **kwargs) -> object:
        """Update fields of an existing shopping list."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, list_id: int) -> None:
        """Delete a shopping list by primary key."""
        raise NotImplementedError


class AbstractItemRepository(ABC):
    """Interface for item persistence operations."""

    @abstractmethod
    def get_by_list(self, list_id: int):
        """Return all items belonging to a shopping list."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, item_id: int):
        """Return a single item by primary key."""
        raise NotImplementedError

    @abstractmethod
    def create(self, list_id: int, name: str, quantity: int = 1, unit: str = "", notes: str = "") -> object:
        """Persist a new item and return it."""
        raise NotImplementedError

    @abstractmethod
    def update(self, item_id: int, **kwargs) -> object:
        """Update fields of an existing item."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, item_id: int) -> None:
        """Delete an item by primary key."""
        raise NotImplementedError

    @abstractmethod
    def toggle_check(self, item_id: int) -> object:
        """Toggle the checked state of an item and return it."""
        raise NotImplementedError
