from typing import List


class Product:
    """Класс для представления товара."""

    name: str
    description: str
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_dict: dict):
        """Класс-метод для создания объекта Product из словаря."""
        return cls(
            name=product_dict["name"],
            description=product_dict["description"],
            price=product_dict["price"],
            quantity=product_dict["quantity"]
        )

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер с проверкой на положительное значение."""
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    def __str__(self) -> str:
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        """Сложение двух продуктов: цена*количество + цена*количество."""
        if isinstance(other, Product):
            return self.price * self.quantity + other.price * other.quantity
        raise TypeError("Складывать можно только объекты Product")


class Category:
    """Класс для представления категории товаров."""

    name: str
    description: str

    __products: List[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product] = None):
        self.name = name
        self.description = description
        self.__products = products if products else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список и увеличивает счётчик."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий строку со списком товаров."""
        result = ""
        for product in self.__products:
            result += f"{product}\n"
        return result

    def _get_total_quantity(self) -> int:
        """Возвращает общее количество товаров на складе."""
        return sum(product.quantity for product in self.__products)

    def __str__(self) -> str:
        """Строковое представление категории."""
        return f"{self.name}, количество продуктов: {self._get_total_quantity()} шт."