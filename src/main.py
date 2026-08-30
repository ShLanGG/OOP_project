from typing import List


class Product:
    """Класс для представления товара."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str
    products: List[Product]

    # Атрибуты класса для подсчёта количества категорий и товаров
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.products = products

        # Увеличиваем счётчики при создании нового объекта
        Category.category_count += 1
        Category.product_count += len(products)


if __name__ == "__main__":
    # Пример использования (опционально)
    product1 = Product("Ноутбук", "Мощный ноутбук", 50000.0, 10)
    product2 = Product("Мышь", "Беспроводная мышь", 1500.0, 25)
    category = Category("Электроника", "Техника и аксессуары", [product1, product2])
    print(f"Категорий: {Category.category_count}, товаров: {Category.product_count}")