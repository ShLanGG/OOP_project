from typing import List


class Product:
    """Базовый класс для всех продуктов."""

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
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        """Сложение двух продуктов одного класса."""
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс смартфона."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс газонной травы."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс категории товаров."""

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
        """Добавляет продукт в приватный список."""
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер списка товаров в виде строки."""
        result = ""
        for product in self.__products:
            result += f"{product}\n"
        return result

    def _get_total_quantity(self) -> int:
        return sum(product.quantity for product in self.__products)

    def __str__(self) -> str:
        return f"{self.name}, количество продуктов: {self._get_total_quantity()} шт."