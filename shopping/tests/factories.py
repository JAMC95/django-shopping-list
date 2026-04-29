"""
Factory Boy factories for test data generation.
Following TDD best practices: factories make tests readable and DRY.
"""
import factory

from shopping.models import Item, ShoppingList


class ShoppingListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShoppingList

    name = factory.Sequence(lambda n: f"Lista de la compra #{n}")
    description = factory.Faker("sentence", locale="es_ES")
    is_completed = False


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    shopping_list = factory.SubFactory(ShoppingListFactory)
    name = factory.Faker("word", locale="es_ES")
    quantity = factory.Faker("random_int", min=1, max=10)
    unit = factory.Iterator(["kg", "litros", "unidades", "g", ""])
    is_checked = False
    notes = ""
