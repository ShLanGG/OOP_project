import pytest
from src.main import Product, Category


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасываем счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product("Смартфон", "Современный смартфон", 30000.0, 15)
    assert product.name == "Смартфон"
    assert product.description == "Современный смартфон"
    assert product.price == 30000.0
    assert product.quantity == 15


def test_category_initialization():
    product1 = Product("Книга", "Роман", 500.0, 100)
    product2 = Product("Ручка", "Синяя", 20.0, 500)
    category = Category("Канцтовары", "Товары для офиса", [product1, product2])
    assert category.name == "Канцтовары"
    assert category.description == "Товары для офиса"
    # Проверяем, что товары добавлены (через геттер)
    products_str = category.products
    assert "Книга, 500.0 руб. Остаток: 100 шт." in products_str
    assert "Ручка, 20.0 руб. Остаток: 500 шт." in products_str


def test_add_product():
    product = Product("Тетрадь", "48 листов", 50.0, 30)
    category = Category("Канцтовары", "Описание", [])
    assert Category.product_count == 0

    category.add_product(product)

    assert Category.product_count == 1
    assert "Тетрадь, 50.0 руб. Остаток: 30 шт." in category.products


def test_new_product_classmethod():
    data = {
        "name": "Монитор",
        "description": "24 дюйма",
        "price": 15000.0,
        "quantity": 10
    }
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert product.name == "Монитор"
    assert product.price == 15000.0
    assert product.quantity == 10


def test_price_setter_positive():
    product = Product("Тест", "Описание", 100.0, 1)
    product.price = 150.0
    assert product.price == 150.0


def test_price_setter_negative(capsys):
    product = Product("Тест", "Описание", 100.0, 1)
    product.price = -50.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 100.0  # цена не изменилась


def test_category_product_count_increment():
    product1 = Product("Товар 1", "Описание", 10.0, 5)
    product2 = Product("Товар 2", "Описание", 20.0, 8)
    Category("Категория 1", "Описание", [product1, product2])
    Category("Категория 2", "Описание", [])
    assert Category.product_count == 2