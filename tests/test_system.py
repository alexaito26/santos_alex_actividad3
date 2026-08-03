import unittest
from bookstore.inventory import Inventory
from bookstore.cart import Cart
from bookstore.order_processor import OrderProcessor, PaymentGateway

# ==========================================
# PRUEBAS DE SISTEMA (System / End-to-End Tests)
# ==========================================

class TestSystem(unittest.TestCase):
    def test_complete_bookstore_flow_system(self):
        """
        Prueba de Sistema: Flujo de principio a fin (E2E).
        Verifica el comportamiento de todo el sistema integrado (Inventario, Carrito y Compra)
        trabajando de forma conjunta bajo un escenario de flujo completo de usuario.
        """
        # 1. Configuración del Entorno del Sistema
        inventory = Inventory()
        payment_gateway = PaymentGateway()  # Usamos la pasarela de pago real (simulador completo)
        processor = OrderProcessor(inventory, payment_gateway)

        # 2. Inicializar base de datos de libros (Stock del Sistema)
        inventory.add_book("978-01", "Don Quijote de la Mancha", 15.50, 20)
        inventory.add_book("978-02", "Cien años de soledad", 22.00, 15)
        inventory.add_book("978-03", "La Metamorfosis", 10.00, 5)

        # 3. Flujo del Usuario 1: Navegar y comprar
        cart = Cart()
        
        # El usuario añade libros al carrito
        cart.add_item("978-01", 1)  # 1 Quijote ($15.50)
        cart.add_item("978-02", 2)  # 2 Cien años ($44.00)
        cart.add_item("978-03", 1)  # 1 Metamorfosis ($10.00)
        
        # El usuario cambia de opinión y quita un libro del carrito
        cart.remove_item("978-03", 1)  # Quita La Metamorfosis por completo

        # Total esperado en el carrito: $15.50 + $44.00 = $59.50
        self.assertEqual(cart.get_total(inventory), 59.50)

        # 4. El usuario realiza la compra (Checkout del Sistema)
        receipt = processor.checkout(cart)

        # 5. Verificaciones de Sistema (Estado final global)
        # A. Verificación del recibo de compra
        self.assertEqual(receipt["status"], "COMPLETED")
        self.assertEqual(receipt["total_paid"], 59.50)
        self.assertEqual(receipt["items"], {"978-01": 1, "978-02": 2})

        # B. Verificación del stock remanente en el inventario global
        # Quijote: inició con 20, compramos 1 -> quedan 19
        self.assertEqual(inventory.get_stock("978-01"), 19)
        # Cien años: inició con 15, compramos 2 -> quedan 13
        self.assertEqual(inventory.get_stock("978-02"), 13)
        # Metamorfosis: inició con 5, no compramos -> quedan 5
        self.assertEqual(inventory.get_stock("978-03"), 5)


if __name__ == '__main__':
    unittest.main()
