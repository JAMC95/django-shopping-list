from django.contrib import admin

from .models import Item, ShoppingList


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
    fields = ("name", "quantity", "unit", "is_checked", "notes")


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("name", "is_completed", "total_items", "checked_items", "created_at")
    list_filter = ("is_completed", "created_at")
    search_fields = ("name", "description")
    inlines = [ItemInline]
    actions = ["mark_as_completed"]

    @admin.action(description="Marcar como completadas")
    def mark_as_completed(self, request, queryset):
        for shopping_list in queryset:
            shopping_list.mark_as_completed()


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "shopping_list", "quantity", "unit", "is_checked", "created_at")
    list_filter = ("is_checked", "shopping_list")
    search_fields = ("name", "notes")
