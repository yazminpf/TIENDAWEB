from decimal import Decimal
from productos.models import Producto

def carrito_info(request):
    carrito = request.session.get('carrito', {})
    total_items = 0
    total_pagar = Decimal('0.00')

    for producto_id_str, item in carrito.items():
        try:
            producto = Producto.objects.get(id=int(producto_id_str))
            cantidad = item.get('cantidad', 0)
            total_items += cantidad
            total_pagar += producto.precio * cantidad
        except:
            continue

    return {
        'cantidad_carrito': total_items,
        'total_carrito': total_pagar
    }