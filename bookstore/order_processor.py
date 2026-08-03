class PaymentGateway:
    """
    Simulación de una pasarela de pagos externa (ej. Stripe o PayPal).
    En pruebas unitarias y de integración, esta clase suele ser mockeada
    para evitar llamadas de red reales o transacciones falsas.
    """
    def charge(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("El monto a cobrar debe ser mayor a cero.")
        # Simula el procesamiento de pago (en producción aquí iría una API call)
        print(f"[PaymentGateway] Cobrando ${amount:.2f} de forma exitosa...")
        return True


class OrderProcessor:
    def __init__(self, inventory, payment_gateway: PaymentGateway):
        self.inventory = inventory
        self.payment_gateway = payment_gateway

    def checkout(self, cart) -> dict:
        items = cart.get_items()
        if not items:
            raise ValueError("No se puede procesar un carrito vacío.")

        # 1. Validar disponibilidad de stock antes de cobrar
        for isbn, quantity in items.items():
            available_stock = self.inventory.get_stock(isbn)
            if available_stock < quantity:
                title = self.inventory.get_title(isbn)
                raise ValueError(
                    f"Stock insuficiente para '{title}'. Requerido: {quantity}, Disponible: {available_stock}"
                )

        # 2. Calcular total
        total = cart.get_total(self.inventory)

        # 3. Procesar el pago a través de la pasarela
        payment_success = self.payment_gateway.charge(total)
        if not payment_success:
            raise RuntimeError("El pago fue rechazado por la pasarela de pagos.")

        # 4. Reducir stock del inventario
        for isbn, quantity in items.items():
            self.inventory.reduce_stock(isbn, quantity)

        # 5. Retornar confirmación de compra
        return {
            "status": "COMPLETED",
            "total_paid": total,
            "items": items
        }
