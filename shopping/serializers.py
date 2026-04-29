"""
DRF serializers — responsible only for data validation and representation
(Single Responsibility Principle).
"""
from rest_framework import serializers

from .models import Item, ShoppingList


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "quantity",
            "unit",
            "is_checked",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ShoppingListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    checked_items = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingList
        fields = [
            "id",
            "name",
            "description",
            "is_completed",
            "total_items",
            "checked_items",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_total_items(self, obj) -> int:
        return obj.total_items()

    def get_checked_items(self, obj) -> int:
        return obj.checked_items()


class ShoppingListCreateSerializer(serializers.ModelSerializer):
    """Minimal serializer for creating/updating a shopping list."""

    class Meta:
        model = ShoppingList
        fields = ["name", "description"]
