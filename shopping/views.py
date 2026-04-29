"""
API Views using Django REST Framework ViewSets.

Each ViewSet delegates all business logic to the service layer,
keeping views thin (Single Responsibility Principle).
Dependency injection is used for the service so views are testable.
"""

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .repositories.shopping_repository import (DjangoItemRepository,
                                               DjangoShoppingListRepository)
from .serializers import (ItemSerializer, ShoppingListCreateSerializer,
                          ShoppingListSerializer)
from .services.shopping_service import ItemService, ShoppingListService


def _get_list_service() -> ShoppingListService:
    """Factory function — enables easy swapping in tests."""
    return ShoppingListService(DjangoShoppingListRepository())


def _get_item_service() -> ItemService:
    return ItemService(DjangoItemRepository(), DjangoShoppingListRepository())


class ShoppingListViewSet(viewsets.ViewSet):
    """
    CRUD endpoint for shopping lists.

    list:   GET  /api/v1/lists/
    create: POST /api/v1/lists/
    retrieve: GET /api/v1/lists/{id}/
    update: PUT  /api/v1/lists/{id}/
    destroy: DELETE /api/v1/lists/{id}/
    complete: POST /api/v1/lists/{id}/complete/
    """

    def list(self, request):
        service = _get_list_service()
        qs = service.get_all_lists()
        serializer = ShoppingListSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ShoppingListCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = _get_list_service()
        try:
            shopping_list = service.create_list(**serializer.validated_data)
        except ValidationError as exc:
            return Response({"detail": exc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            ShoppingListSerializer(shopping_list).data, status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        service = _get_list_service()
        try:
            shopping_list = service.get_list(int(pk))
        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ShoppingListSerializer(shopping_list).data)

    def update(self, request, pk=None):
        serializer = ShoppingListCreateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service = _get_list_service()
        try:
            shopping_list = service.update_list(int(pk), **serializer.validated_data)
        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as exc:
            return Response({"detail": exc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ShoppingListSerializer(shopping_list).data)

    def destroy(self, request, pk=None):
        service = _get_list_service()
        try:
            service.delete_list(int(pk))
        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """Mark a shopping list as completed."""
        service = _get_list_service()
        try:
            shopping_list = service.complete_list(int(pk))
        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ShoppingListSerializer(shopping_list).data)


class ItemViewSet(viewsets.ViewSet):
    """
    CRUD endpoint for items within a shopping list.

    list:   GET  /api/v1/lists/{list_pk}/items/
    create: POST /api/v1/lists/{list_pk}/items/
    retrieve: GET /api/v1/lists/{list_pk}/items/{id}/
    update: PUT  /api/v1/lists/{list_pk}/items/{id}/
    destroy: DELETE /api/v1/lists/{list_pk}/items/{id}/
    toggle: POST /api/v1/lists/{list_pk}/items/{id}/toggle/
    """

    def list(self, request, list_pk=None):
        service = _get_item_service()
        try:
            items = service.get_items_for_list(int(list_pk))
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Shopping list not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(ItemSerializer(items, many=True).data)

    def create(self, request, list_pk=None):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = _get_item_service()
        data = serializer.validated_data
        try:
            item = service.add_item(
                list_id=int(list_pk),
                name=data["name"],
                quantity=data.get("quantity", 1),
                unit=data.get("unit", ""),
                notes=data.get("notes", ""),
            )
        except (ObjectDoesNotExist, ValidationError) as exc:
            msg = exc.message if isinstance(exc, ValidationError) else str(exc)
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, list_pk=None):
        service = _get_item_service()
        try:
            item = service.get_item(int(pk))
        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ItemSerializer(item).data)

    def update(self, request, pk=None, list_pk=None):
        serializer = ItemSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service = _get_item_service()
        try:
            item = service.update_item(int(pk), **serializer.validated_data)
        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as exc:
            return Response({"detail": exc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ItemSerializer(item).data)

    def destroy(self, request, pk=None, list_pk=None):
        service = _get_item_service()
        try:
            service.delete_item(int(pk))
        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def toggle(self, request, pk=None, list_pk=None):
        """Toggle the checked state of an item."""
        service = _get_item_service()
        try:
            item = service.toggle_item(int(pk))
        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ItemSerializer(item).data)
