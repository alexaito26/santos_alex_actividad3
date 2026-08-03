class Cart:
    def __init__(self):
        # Almacena los ítems del carrito: {isbn: cantidad}
        self._items = {}
        self._discount_code = None

    def add_item(self, isbn: str, quantity: int):
        if quantity <= 0:
            raise ValueError("La cantidad a agregar debe ser mayor a cero.")
        
        self._items[isbn] = self._items.get(isbn, 0) + quantity

    def remove_item(self, isbn: str, quantity: int = None):
        if isbn not in self._items:
            raise ValueError(f"El libro con ISBN {isbn} no está en el carrito.")
        
        if quantity is None or quantity >= self._items[isbn]:
            del self._items[isbn]
        else:
            if quantity <= 0:
                raise ValueError("La cantidad a remover debe ser mayor a cero.")
            self._items[isbn] -= quantity

    def get_items(self) -> dict:
        return self._items.copy()

    def apply_coupon(self, code: str):
        """Guarda el cupón de descuento ingresado por el cliente."""
        self._discount_code = code

    def get_total(self, inventory) -> float:
        """
        Calcula el total del carrito interactuando con un objeto de inventario.
        Esta interacción es clave para demostrar pruebas de integración y mocks.
        Si el cupón es DESCUENTO10, aplica un 10% de descuento sobre el total.
        """
        total = 0.0
        for isbn, quantity in self._items.items():
            price = inventory.get_price(isbn)
            total += price * quantity

        if self._discount_code == "DESCUENTO10":
            total *= 0.9

        return total
