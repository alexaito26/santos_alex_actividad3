import unittest
from unittest.mock import Mock
from bookstore.inventory import Inventory
from bookstore.cart import Cart
from bookstore.order_processor import OrderProcessor

# ==========================================
# PRUEBAS DE INTEGRACIÓN (Integration Tests)
# ==========================================

class TestIntegration(unittest.TestCase):
    def test_cart_and_inventory_integration(self):
        """
        Prueba de Integración: Verifica que la clase Cart y la clase Inventory
        funcionan juntas de forma correcta sin usar mocks para Inventory.
        """
        # 1. Instanciar módulos reales
        inventory = Inventory()
        cart = Cart()

        # 2. Configurar estado del inventario real
        inventory.add_book("123", "Harry Potter", 20.00, 10)
        inventory.add_book("456", "El Principito", 10.00, 5)

        # 3. Operar con el carrito
        cart.add_item("123", 2)
        cart.add_item("456", 1)

        # 4. Verificar integración: Cart calcula total pidiendo precios reales a Inventory
        # Total esperado: (2 * 20.00) + (1 * 10.00) = 50.00
        self.assertEqual(cart.get_total(inventory), 50.00)

    def test_order_processor_integration_with_real_inventory(self):
        """
        Prueba de Integración: Verifica que OrderProcessor y Inventory funcionan juntos.
        
        Al completar una compra exitosa, el inventario real de los libros comprados
        debe reducirse en la cantidad correspondiente.
        """
        # 1. Configurar módulos reales
        inventory = Inventory()
        inventory.add_book("999", "Python Avanzado", 50.00, 5)
        
        cart = Cart()
        cart.add_item("999", 2)

        # Mock de PaymentGateway: Mockeamos el servicio externo (ej. pasarela bancaria)
        # pero mantenemos los módulos internos de nuestra app reales.
        mock_payment = Mock()
        mock_payment.charge.return_value = True

        # Aplicar cupón de descuento en el carrito (inventario real + OrderProcessor)
        cart.apply_coupon("DESCUENTO10")

        processor = OrderProcessor(inventory, mock_payment)

        # 2. Procesar compra
        result = processor.checkout(cart)

        # 3. Verificar efectos de la integración
        self.assertEqual(result["status"], "COMPLETED")
        # (2 * 50.00) = 100.00 con 10% de descuento => 90.00
        self.assertEqual(result["total_paid"], 90.00)
        
        # ¡La integración redujo el stock en el inventario real!
        # El stock inicial era 5, compramos 2, debe quedar 3.
        self.assertEqual(inventory.get_stock("999"), 3)

    def test_order_processor_integration_insufficient_stock_rollback(self):
        """
        Prueba de Integración: Verifica la lógica conjunta cuando hay una falla.
        Si se intenta procesar una compra y un artículo no tiene suficiente stock,
        el proceso debe lanzar un error y el stock de los demás artículos no debe verse afectado.
        """
        inventory = Inventory()
        inventory.add_book("A1", "Libro con stock", 10.00, 10)
        inventory.add_book("B2", "Libro sin stock", 15.00, 0)

        cart = Cart()
        cart.add_item("A1", 2)
        cart.add_item("B2", 1)  # No hay stock de este

        mock_payment = Mock()
        processor = OrderProcessor(inventory, mock_payment)

        # Intentar procesar la compra debe lanzar error
        with self.assertRaisesRegex(ValueError, "Stock insuficiente para 'Libro sin stock'"):
            processor.checkout(cart)

        # Verificar que el stock de A1 no se haya reducido (efecto rebote/rollback)
        self.assertEqual(inventory.get_stock("A1"), 10)
        # Verificar que no se llamó al cobro
        mock_payment.charge.assert_not_called()


if __name__ == '__main__':
    unittest.main()
