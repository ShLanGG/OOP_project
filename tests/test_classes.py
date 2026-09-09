import pytest
from src.main import Product, Category, Smartphone, LawnGrass, BaseProduct, MixinLog


@pytest.fixture(autouse=True)
def reset_category_counters():
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


def test_new_product_with_zero_quantity():
    data = {"name": "Тест", "description": "Описание", "price": 100.0, "quantity": 0}
    with pytest.raises(ValueError):
        Product.new_product(data)


def test_price_setter_positive():
    product = Product("Тест", "Описание", 100.0, 1)
    product.price = 150.0
    assert product.price == 150.0


def test_price_setter_negative(capsys):
    product = Product("Тест", "Описание", 100.0, 1)
    product.price = -50.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 100.0


def test_price_setter_zero(capsys):
    product = Product("Тест", "Описание", 100.0, 1)
    product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 100.0


def test_category_product_count_increment():
    product1 = Product("Товар 1", "Описание", 10.0, 5)
    product2 = Product("Товар 2", "Описание", 20.0, 8)
    Category("Категория 1", "Описание", [product1, product2])
    Category("Категория 2", "Описание", [])
    assert Category.product_count == 2


def test_product_str():
    product = Product("Ноутбук", "Мощный", 80000.0, 3)
    assert str(product) == "Ноутбук, 80000.0 руб. Остаток: 3 шт."


def test_category_str():
    product1 = Product("Телефон", "Смартфон", 50000.0, 2)
    product2 = Product("Чехол", "Силиконовый", 500.0, 5)
    category = Category("Электроника", "Разное", [product1, product2])
    assert str(category) == "Электроника, количество продуктов: 7 шт."


def test_product_add_same_class():
    product1 = Product("Товар1", "Описание1", 100.0, 10)
    product2 = Product("Товар2", "Описание2", 200.0, 2)
    assert product1 + product2 == 1400.0


def test_product_add_with_non_product():
    product = Product("Товар", "Описание", 100.0, 1)
    with pytest.raises(TypeError):
        product + "не товар"


def test_mixin_log_on_product_creation(capsys):
    Product("Тест", "Описание", 100.0, 1)
    captured = capsys.readouterr()
    assert "Создан объект класса Product" in captured.out
    assert "('Тест', 'Описание', 100.0, 1)" in captured.out


def test_mixin_log_on_smartphone_creation(capsys):
    Smartphone("iPhone", "Смартфон", 1000.0, 1, "A15", "13", 128, "black")
    captured = capsys.readouterr()
    assert "Создан объект класса Smartphone" in captured.out


def test_mixin_log_on_lawngrass_creation(capsys):
    LawnGrass("Grass", "Трава", 10.0, 1, "Russia", 7, "green")
    captured = capsys.readouterr()
    assert "Создан объект класса LawnGrass" in captured.out


def test_baseproduct_is_abstract():
    with pytest.raises(TypeError):
        BaseProduct("Test", "Desc", 100, 1)


def test_inheritance_chain():
    assert issubclass(Product, BaseProduct)
    assert issubclass(Product, MixinLog)
    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)


def test_smartphone_attributes():
    phone = Smartphone("Phone", "Desc", 1000.0, 1, "eff", "model", 128, "black")
    assert phone.efficiency == "eff"
    assert phone.model == "model"
    assert phone.memory == 128
    assert phone.color == "black"


def test_lawngrass_attributes():
    grass = LawnGrass("Grass", "Desc", 10.0, 1, "Russia", 7, "green")
    assert grass.country == "Russia"
    assert grass.germination_period == 7
    assert grass.color == "green"


def test_add_smartphone_and_lawngrass_raises_typeerror():
    phone = Smartphone("Phone", "desc", 1000.0, 1, "eff", "model", 64, "black")
    grass = LawnGrass("Grass", "desc", 100.0, 1, "country", 7, "green")
    with pytest.raises(TypeError):
        phone + grass


def test_add_same_subclass_works():
    phone1 = Smartphone("Phone1", "desc", 1000.0, 2, "eff", "model", 64, "black")
    phone2 = Smartphone("Phone2", "desc", 2000.0, 1, "eff", "model", 128, "white")
    assert phone1 + phone2 == 1000.0 * 2 + 2000.0 * 1


def test_add_product_with_non_product_raises():
    category = Category("Test", "Desc", [])
    with pytest.raises(TypeError):
        category.add_product("не продукт")


def test_add_product_accepts_subclass():
    category = Category("Test", "Desc", [])
    phone = Smartphone("Phone", "desc", 1000.0, 1, "eff", "model", 64, "black")
    category.add_product(phone)
    assert Category.product_count == 1
    assert "Phone" in category.products


def test_product_zero_quantity_raises_valueerror():
    with pytest.raises(ValueError) as exc_info:
        Product("Тест", "Описание", 100.0, 0)
    assert str(exc_info.value) == "Товар с нулевым количеством не может быть добавлен"


def test_category_average_price_normal():
    product1 = Product("Товар1", "Описание", 100.0, 2)
    product2 = Product("Товар2", "Описание", 200.0, 3)
    category = Category("Категория", "Описание", [product1, product2])
    assert category.average_price() == 150.0


def test_category_average_price_empty():
    category = Category("Пустая", "Описание", [])
    assert category.average_price() == 0