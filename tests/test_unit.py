import unittest
from unittest.mock import Mock
from bookstore.inventory import Inventory
from bookstore.cart import Cart

# ==========================================
# PRUEBAS UNITARIAS: INVENTARIO (Inventory)
# ==========================================

class TestInventory(unittest.TestCase):
    def test_inventory_add_book_success(self):
        """Prueba unitaria: Agregar un libro al inventario con datos válidos."""
        inventory = Inventory()
        inventory.add_book("123-456", "El Quijote", 19.99, 10)
        
        self.assertEqual(inventory.get_stock("123-456"), 10)
        self.assertEqual(inventory.get_price("123-456"), 19.99)
        self.assertEqual(inventory.get_title("123-456"), "El Quijote")

    def test_inventory_add_book_negative_price(self):
        """Prueba unitaria: Intentar agregar un libro con precio negativo debe lanzar ValueError."""
        inventory = Inventory()
        with self.assertRaisesRegex(ValueError, "El precio no puede ser negativo."):
            inventory.add_book("123-456", "El Quijote", -5.00, 10)

    def test_inventory_reduce_stock_insufficient(self):
        """Prueba unitaria: Reducir más stock del disponible debe lanzar ValueError."""
        inventory = Inventory()
        inventory.add_book("123-456", "El Quijote", 19.99, 5)
        
        with self.assertRaisesRegex(ValueError, "Stock insuficiente"):
            inventory.reduce_stock("123-456", 10)


# ==========================================
# PRUEBAS UNITARIAS: CARRITO (Cart)
# ==========================================

class TestCart(unittest.TestCase):
    def test_cart_add_item_new(self):
        """Prueba unitaria: Agregar un nuevo producto al carrito."""
        cart = Cart()
        cart.add_item("123-456", 2)
        self.assertEqual(cart.get_items(), {"123-456": 2})

    def test_cart_add_item_existing(self):
        """Prueba unitaria: Incrementar la cantidad de un producto ya existente en el carrito."""
        cart = Cart()
        cart.add_item("123-456", 2)
        cart.add_item("123-456", 3)
        self.assertEqual(cart.get_items(), {"123-456": 5})

    def test_cart_remove_item_partial(self):
        """Prueba unitaria: Remover parcialmente un producto del carrito."""
        cart = Cart()
        cart.add_item("123-456", 5)
        cart.remove_item("123-456", 2)
        self.assertEqual(cart.get_items(), {"123-456": 3})

    def test_cart_remove_item_full(self):
        """Prueba unitaria: Remover completamente un producto del carrito."""
        cart = Cart()
        cart.add_item("123-456", 5)
        cart.remove_item("123-456")  # Sin cantidad especificada, elimina todo
        self.assertEqual(cart.get_items(), {})

    def test_cart_get_total_with_discount_coupon_using_mock(self):
        """
        Prueba unitaria: Calcular el total del carrito con un código de descuento usando un MOCK de Inventario.
        
        ¿Por qué es una prueba unitaria?
        Porque estamos aislando la clase Cart. No usamos la base de datos ni el código real
        de la clase Inventory. Simulamos el comportamiento de Inventory.get_price.
        """
        # 1. Crear el carrito e ingresar ítems
        cart = Cart()
        cart.add_item("111-222", 2)
        cart.add_item("333-444", 1)
        
        # 2. Aplicar un código de descuento
        cart.apply_coupon("DESCUENTO10")

        # 3. Crear un objeto Mock de la clase Inventory
        mock_inventory = Mock()
        
        # 4. Definir lo que retornará el método get_price cuando sea llamado
        def mock_get_price(isbn):
            if isbn == "111-222":
                return 10.0
            elif isbn == "333-444":
                return 25.0
            return 0.0

        mock_inventory.get_price.side_effect = mock_get_price

        # 5. Ejecutar el método a probar
        total = cart.get_total(mock_inventory)

        # 6. Verificar: (2 * $10.0 + 1 * $25.0) * 0.9 (descuento del 10%) = $40.5
        self.assertEqual(total, 40.5)
        
        # Verificar que el mock fue llamado correctamente para cada ISBN
        mock_inventory.get_price.assert_any_call("111-222")
        mock_inventory.get_price.assert_any_call("333-444")
        self.assertEqual(mock_inventory.get_price.call_count, 2)

    def test_cart_get_total_with_mock_inventory(self):
        """
        Prueba unitaria crucial: Calcular el total del carrito usando un MOCK de Inventario.
        
        ¿Por qué es una prueba unitaria?
        Porque estamos aislando la clase Cart. No usamos la base de datos ni el código real
        de la clase Inventory. Simulamos el comportamiento de Inventory.get_price.
        """
        # 1. Crear el carrito e ingresar ítems
        cart = Cart()
        cart.add_item("111-222", 2)
        cart.add_item("333-444", 1)

        # 2. Crear un objeto Mock de la clase Inventory
        mock_inventory = Mock()
        
        # 3. Definir lo que retornará el método get_price cuando sea llamado
        def mock_get_price(isbn):
            if isbn == "111-222":
                return 10.0
            elif isbn == "333-444":
                return 25.0
            return 0.0

        mock_inventory.get_price.side_effect = mock_get_price

        # 4. Ejecutar el método a probar
        total = cart.get_total(mock_inventory)

        # 5. Verificar: (2 * $10.0) + (1 * $25.0) = $45.0
        self.assertEqual(total, 45.0)
        
        # Verificar que el mock fue llamado correctamente para cada ISBN
        mock_inventory.get_price.assert_any_call("111-222")
        mock_inventory.get_price.assert_any_call("333-444")
        self.assertEqual(mock_inventory.get_price.call_count, 2)


if __name__ == '__main__':
    unittest.main()
