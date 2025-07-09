from django.contrib import admin

from .models import Producto
from .models import Categoria
from .models import ImagenProducto

admin.site.register(Categoria)

admin.site.register(Producto)
admin.site.register(ImagenProducto)