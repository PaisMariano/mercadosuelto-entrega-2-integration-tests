API Integration Test Suite

Este proyecto contiene un conjunto de pruebas automatizadas para validar la integración de dos microservicios REST relacionados con la gestión de Productos, Usuarios y Vendedores (Sellers).
Descripción

El script de pruebas realiza operaciones CRUD (Create, Read, Update, Delete) sobre las siguientes entidades:

    Usuarios (Users)

    Vendedores (Sellers)

    Productos (Products)

    Ventas (Sales)

A través de estas pruebas, se asegura que los endpoints de ambos microservicios funcionan correctamente bajo distintas situaciones de uso.
Endpoints base

Productos / Categorías : http://localhost:8080/api/v1

Sellers / Users	: http://localhost:8081/api/v1


Requisitos

    Python 3.8+

    Librería requests y pytest


Instalación de dependencias:

    pip install requests

    pip install pytest


Estructura de las pruebas

Las pruebas cubren:

Productos

    Crear un producto.

    Obtener todos los productos.

    Eliminar todos los productos.

    Verificar la creación y eliminación de un producto.

    Simular el proceso de venta de un producto.

Usuarios

    Crear un usuario.

    Obtener todos los usuarios.

    Verificar la creación y eliminación de un usuario.

Vendedores (Sellers)

    Crear un seller.

    Obtener todos los sellers.

    Actualizar información de un seller.

    Eliminar sellers.

    Verificar la creación y eliminación de un seller.

Ejecución de pruebas

pytest nombre_del_archivo.py

Limpieza de datos

Cada prueba que crea datos (usuarios, productos o sellers) también incluye una fase de limpieza que elimina los datos creados para mantener los microservicios sin residuos.

Consideraciones

    Ambos microservicios deben estar levantados en los puertos especificados antes de correr las pruebas.

    Estas pruebas asumen que los endpoints devuelven códigos HTTP estándar (200, 201, 204, 404).
