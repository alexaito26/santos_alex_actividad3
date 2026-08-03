import unittest
from bookstore.inventory import Inventory
from bookstore.cart import Cart
from bookstore.order_processor import OrderProcessor, PaymentGateway

# ==========================================
# PRUEBAS DE ACEPTACIÓN DE USUARIO (UAT)
# ==========================================

class TestUAT(unittest.TestCase):
    def test_uat_compra_exitosa_por_cliente(self):
        """
        Historia de Usuario:
        Como cliente de la librería,
        Quiero agregar un libro disponible al carrito y pagarlo con éxito,
        Para poder asegurar mi compra y recibir mis libros.
        
        Criterio de Aceptación (Escenario Feliz):
        - Dado que en la librería existe el libro 'Harry Potter' con 5 unidades en stock y cuesta $20.
        - Cuando el cliente agrega 2 unidades al carrito y procesa el pago.
        - Entonces el pedido debe completarse exitosamente, cobrando $40, y el stock final debe ser 3.
        """
        # GIVEN (Dado que...)
        libreria = Inventory()
        libreria.add_book("HP-01", "Harry Potter y la Piedra Filosofal", 20.00, 5)
        
        pasarela_pagos = PaymentGateway()
        procesador = OrderProcessor(libreria, pasarela_pagos)
        
        carrito = Cart()

        # WHEN (Cuando...)
        carrito.add_item("HP-01", 2)
        resultado_compra = procesador.checkout(carrito)

        # THEN (Entonces...)
        self.assertEqual(resultado_compra["status"], "COMPLETED")
        self.assertEqual(resultado_compra["total_paid"], 40.00)
        self.assertEqual(libreria.get_stock("HP-01"), 3)

    def test_uat_compra_rechazada_por_falta_de_stock(self):
        """
        Historia de Usuario:
        Como administrador de la librería,
        Quiero que el sistema rechace compras si el cliente pide más stock del disponible,
        Para evitar vender libros que no tenemos físicamente.
        
        Criterio de Aceptación:
        - Dado que el libro 'El Principito' tiene 1 sola unidad en stock.
        - Cuando un cliente intenta comprar 2 unidades de ese libro.
        - Entonces el sistema debe rechazar la transacción con un mensaje claro de falta de stock,
          y el stock del libro debe mantenerse en 1 (no debe haber cobro ni descuento de inventario).
        """
        # GIVEN (Dado que...)
        libreria = Inventory()
        libreria.add_book("PR-02", "El Principito", 12.00, 1)
        
        pasarela_pagos = PaymentGateway()
        procesador = OrderProcessor(libreria, pasarela_pagos)
        
        carrito = Cart()

        # WHEN (Cuando...)
        carrito.add_item("PR-02", 2)  # Intenta comprar 2, pero solo hay 1

        # THEN (Entonces...)
        # Esperamos que falle lanzando una excepción controlada
        with self.assertRaisesRegex(ValueError, "Stock insuficiente para 'El Principito'"):
            procesador.checkout(carrito)
            
        # El stock del sistema debe seguir intacto en 1
        self.assertEqual(libreria.get_stock("PR-02"), 1)


    def test_uat_compra_con_descuento_exitoso(self):
        """
        Historia de Usuario:
        Como cliente de la librería,
        Quiero aplicar un código de descuento válido al carrito,
        Para obtener un precio reducido en mi compra.
        
        Criterio de Aceptación:
        - Dado que tengo en inventario 'El Principito' con 1 unidad a $10.00.
        - Cuando el cliente lo agrega al carrito, aplica el cupón 'DESCUENTO10' y completa el checkout.
        - Entonces el cobro final realizado debe ser exactamente por $9.00 y el stock debe quedar en 0.
        """
        # GIVEN (Dado que...)
        libreria = Inventory()
        libreria.add_book("PR-02", "El Principito", 10.00, 1)
        
        pasarela_pagos = PaymentGateway()
        procesador = OrderProcessor(libreria, pasarela_pagos)
        
        carrito = Cart()

        # WHEN (Cuando...)
        carrito.add_item("PR-02", 1)
        carrito.apply_coupon("DESCUENTO10")
        resultado_compra = procesador.checkout(carrito)

        # THEN (Entonces...)
        self.assertEqual(resultado_compra["status"], "COMPLETED")
        self.assertEqual(resultado_compra["total_paid"], 9.00)
        self.assertEqual(libreria.get_stock("PR-02"), 0)


if __name__ == '__main__':
    unittest.main()
