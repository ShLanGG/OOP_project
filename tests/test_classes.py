import pytest
from main import Product, Category


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасываем счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    """Проверка корректной инициализации объекта Product."""
    product = Product("Смартфон", "Современный смартфон", 30000.0, 15)
    assert product.name == "Смартфон"
    assert product.description == "Современный смартфон"
    assert product.price == 30000.0
    assert product.quantity == 15


def test_category_initialization():
    """Проверка корректной инициализации объекта Category."""
    product1 = Product("Книга", "Роман", 500.0, 100)
    product2 = Product("Ручка", "Синяя", 20.0, 500)
    category = Category("Канцтовары", "Товары для офиса", [product1, product2])
    assert category.name == "Канцтовары"
    assert category.description == "Товары для офиса"
    assert len(category.products) == 2
    assert isinstance(category.products[0], Product)
    assert isinstance(category.products[1], Product)


def test_category_count_increment():
    """Проверка подсчёта количества категорий."""
    # Начальное значение 0 (сброшено фикстурой)
    assert Category.category_count == 0

    product = Product("Товар", "Описание", 100.0, 1)
    Category("Категория 1", "Описание", [product])
    Category("Категория 2", "Описание", [])
    Category("Категория 3", "Описание", [product, product])

    assert Category.category_count == 3


def test_product_count_increment():
    """Проверка подсчёта количества товаров (длина списка продуктов)."""
    product1 = Product("Товар 1", "Описание", 10.0, 5)
    product2 = Product("Товар 2", "Описание", 20.0, 8)
    product3 = Product("Товар 3", "Описание", 30.0, 2)

    Category("Категория 1", "Описание", [product1, product2])
    Category("Категория 2", "Описание", [product3])
    Category("Категория 3", "Описание", [])

    assert Category.product_count == 3  # 2 + 1 + 0