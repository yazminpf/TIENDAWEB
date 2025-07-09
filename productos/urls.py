from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar/<int:producto_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
]