
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto, Carrito, ItemCarrito
from decimal import Decimal

from .models import Producto, Categoria
from .models import Carrito
from django.db.models import Q

def lista_productos(request):
    categoria_id = request.GET.get('categoria')
   
    busqueda = request.GET.get('q') or ''
    productos = Producto.objects.filter(stock__gt=0)  # 🔥 Solo productos con stock > 0
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    categorias = Categoria.objects.all()
    
    return render(request, 'productos/lista.html', {
        'productos': productos,
         'categorias': categorias,
        'categoria_seleccionada': categoria_id,
        'busqueda': busqueda
                                                    })

def obtener_o_crear_carrito(usuario):
    carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
    return carrito

# 💳 Carrito para usuarios registrados (nuevas vistas)
@login_required
def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    producto_id_str = str(producto_id)

    if producto_id_str in carrito:
        carrito[producto_id_str]['cantidad'] += 1
    else:
        carrito[producto_id_str] = {'cantidad': 1}

    request.session['carrito'] = carrito
    return redirect('ver_carrito')
@login_required
def quitar_del_carrito(request, producto_id):
    carrito = obtener_o_crear_carrito(request.user)
    producto = get_object_or_404(Producto, id=producto_id)
    item = ItemCarrito.objects.filter(carrito=carrito, producto=producto).first()
    if item:
        item.delete()
    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    carrito = obtener_o_crear_carrito(request.user)
    carrito.items.all().delete()
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos_en_carrito = []
    total = Decimal('0.00')

    for producto_id_str, item in carrito.items():
        try:
            producto = Producto.objects.get(id=int(producto_id_str))
            cantidad = int(item.get('cantidad', 0))
            subtotal = cantidad * producto.precio
            total += subtotal
            productos_en_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except Producto.DoesNotExist:
            continue

    return render(request, 'productos/carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'total': total
    })