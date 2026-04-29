"""
Shopping app models.

Design follows:
- Single Responsibility: each model has one clear responsibility.
- Open/Closed: models can be extended without modification.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class ShoppingList(models.Model):
    """Represents a named shopping list."""

    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    is_completed = models.BooleanField(_("completed"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("shopping list")
        verbose_name_plural = _("shopping lists")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    def mark_as_completed(self) -> None:
        """Mark the list as completed."""
        self.is_completed = True
        self.save(update_fields=["is_completed", "updated_at"])

    def total_items(self) -> int:
        """Return the total number of items in this list."""
        return self.items.count()

    def checked_items(self) -> int:
        """Return the number of checked items."""
        return self.items.filter(is_checked=True).count()


class Item(models.Model):
    """Represents a product/item inside a shopping list."""

    shopping_list = models.ForeignKey(
        ShoppingList,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("shopping list"),
    )
    name = models.CharField(_("name"), max_length=255)
    quantity = models.PositiveIntegerField(_("quantity"), default=1)
    unit = models.CharField(
        _("unit"), max_length=50, blank=True, help_text=_("e.g. kg, litres, units")
    )
    is_checked = models.BooleanField(_("checked"), default=False)
    notes = models.TextField(_("notes"), blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")
        ordering = ["is_checked", "name"]

    def __str__(self) -> str:
        if self.unit:
            return f"{self.name} ({self.quantity} {self.unit})"
        return f"{self.name} x{self.quantity}"

    def toggle_check(self) -> None:
        """Toggle the checked state of this item."""
        self.is_checked = not self.is_checked
        self.save(update_fields=["is_checked", "updated_at"])
