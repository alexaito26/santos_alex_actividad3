class Inventory:
    def __init__(self):
        # Almacena libros usando el ISBN como llave.
        # Estructura: {isbn: {"title": str, "price": float, "stock": int}}
        self._books = {}

    def add_book(self, isbn: str, title: str, price: float, stock: int):
        if price < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        
        self._books[isbn] = {
            "title": title,
            "price": price,
            "stock": stock
        }

    def get_stock(self, isbn: str) -> int:
        if isbn not in self._books:
            return 0
        return self._books[isbn]["stock"]

    def get_price(self, isbn: str) -> float:
        if isbn not in self._books:
            raise ValueError(f"El libro con ISBN {isbn} no existe en el inventario.")
        return self._books[isbn]["price"]

    def get_title(self, isbn: str) -> str:
        if isbn not in self._books:
            raise ValueError(f"El libro con ISBN {isbn} no existe en el inventario.")
        return self._books[isbn]["title"]

    def reduce_stock(self, isbn: str, quantity: int):
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser mayor a cero.")
        if isbn not in self._books:
            raise ValueError(f"El libro con ISBN {isbn} no existe en el inventario.")
        
        current_stock = self._books[isbn]["stock"]
        if current_stock < quantity:
            raise ValueError(f"Stock insuficiente para {self._books[isbn]['title']}. Requerido: {quantity}, Disponible: {current_stock}")
        
        self._books[isbn]["stock"] -= quantity
