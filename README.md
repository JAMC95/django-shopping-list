# 🛒 Django Shopping List API

REST API completa para gestionar listas de la compra, construida con **Django 4.2** y **Django REST Framework**.

Proyecto de demostración con énfasis en:

- ✅ **TDD** (Test-Driven Development) — tests escritos antes de la implementación
- 🧱 **Principios SOLID** — Repositorios, Servicios e Inyección de Dependencias
- 🏗️ **Arquitectura por capas** — Models → Repository → Service → View
- 🔍 **Calidad de código** — flake8, black, isort, coverage

---

## Arquitectura

```
config/           Django project settings (base / development)
shopping/
  models.py       Modelos de dominio (ShoppingList, Item)
  repositories/   Patrón repositorio — abstracción sobre el ORM
    interfaces.py       Clases abstractas (DIP)
    shopping_repository.py  Implementación Django ORM
  services/       Lógica de negocio desacoplada de la persistencia
    interfaces.py
    shopping_service.py
  serializers.py  Serialización DRF
  views.py        ViewSets delgados que delegan en servicios
  urls.py         Rutas de la API
  tests/
    factories.py        Factory Boy para datos de prueba
    test_models.py      Tests unitarios de modelos
    test_repositories.py Tests de integración con BD
    test_services.py    Tests unitarios de servicios (sin BD)
    test_views.py       Tests de integración de la API
```

## Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/v1/lists/` | Listar todas las listas |
| POST | `/api/v1/lists/` | Crear una nueva lista |
| GET | `/api/v1/lists/{id}/` | Obtener una lista con sus items |
| PUT | `/api/v1/lists/{id}/` | Actualizar una lista |
| DELETE | `/api/v1/lists/{id}/` | Eliminar una lista |
| POST | `/api/v1/lists/{id}/complete/` | Marcar lista como completada |
| GET | `/api/v1/lists/{id}/items/` | Listar items de una lista |
| POST | `/api/v1/lists/{id}/items/` | Añadir item a una lista |
| GET | `/api/v1/lists/{id}/items/{item_id}/` | Obtener un item |
| PUT | `/api/v1/lists/{id}/items/{item_id}/` | Actualizar un item |
| DELETE | `/api/v1/lists/{id}/items/{item_id}/` | Eliminar un item |
| POST | `/api/v1/lists/{id}/items/{item_id}/toggle/` | Marcar/desmarcar item |

---

## Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/django-shopping-list.git
cd django-shopping-list

# 2. Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt

# 3. Configurar variables de entorno
cp .env.example .env

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario (opcional)
python manage.py createsuperuser

# 6. Lanzar servidor de desarrollo
python manage.py runserver
```

API disponible en: `http://localhost:8000/api/v1/`  
Admin panel: `http://localhost:8000/admin/`

---

## Tests

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
coverage run -m pytest
coverage report -m
coverage html  # Genera htmlcov/index.html

# Tests unitarios de servicios (sin base de datos)
pytest shopping/tests/test_services.py

# Tests de la API
pytest shopping/tests/test_views.py
```

---

## Calidad de código

```bash
# Linting
flake8 .

# Formateo automático
black .

# Ordenar imports
isort .
```

---

## Principios SOLID aplicados

| Principio | Aplicación |
|-----------|-----------|
| **S** — Single Responsibility | Cada clase tiene una sola responsabilidad (Model, Repository, Service, View) |
| **O** — Open/Closed | Nuevos backends de BD → nueva implementación del repositorio, sin modificar servicios |
| **L** — Liskov Substitution | `DjangoShoppingListRepository` es intercambiable por cualquier stub en tests |
| **I** — Interface Segregation | Interfaces separadas para listas e items |
| **D** — Dependency Inversion | Los servicios dependen de abstracciones, no de implementaciones concretas |

---

## Stack tecnológico

- **Python 3.9+**
- **Django 4.2**
- **Django REST Framework 3.16**
- **pytest** + **pytest-django**
- **Factory Boy** para fixtures
- **black** + **flake8** + **isort** para calidad de código
