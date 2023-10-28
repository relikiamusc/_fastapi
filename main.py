# pip install fastapi pydantic unicorn

# Rutas
# http://127.0.0.1:8000/docs/
# http://127.0.0.1:8000/productos/
# http://127.0.0.1:8000/productos/1

# Ejecutar proyecto
# uvicorn main:app --reload

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

# Inicialización de FastAPI
app = FastAPI()

# Modelo de Producto utilizando Pydantic
class Producto(BaseModel):
    id: Optional[int]
    nombre: str
    precio: float
    stock: int

# Base de Datos Falsa (una lista de Python en este caso)
# productos = []
# Añadimos algunos productos ficticios aquí
productos = [
    {"id": 1, "nombre": "Manzana", "precio": 1.2, "stock": 10},
    {"id": 2, "nombre": "Banana", "precio": 0.5, "stock": 20},
    {"id": 3, "nombre": "Cereza", "precio": 2.0, "stock": 15}
]

# Variable para mantener el próximo ID disponible
proximo_id = len(productos)

# Operación para crear un producto (POST)
@app.post("/productos/")
def crear_producto(producto: Producto):
    global proximo_id  # Utilizamos la variable global
    producto = producto.dict()
    producto["id"] = proximo_id  # Asignamos el próximo ID disponible
    productos.append(producto)
    proximo_id += 1  # Incrementamos el ID para el próximo producto
    return producto

# Operación para leer todos los productos (GET)
@app.get("/productos/")
def leer_productos():
    return productos

# Operación para leer un producto individual por ID (GET)
@app.get("/productos/{producto_id}")
def leer_producto(producto_id: int):
    producto = next((item for item in productos if item["id"] == producto_id), None)
    return producto if producto else {"mensaje": "Producto no encontrado"}

# Operación para actualizar un producto por ID (PUT)
@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: Producto):
    producto_actualizado = producto.dict()
    for idx, prod in enumerate(productos):
        if prod["id"] == producto_id:
            producto_actualizado["id"] = producto_id  # Aseguramos que el ID no cambie
            productos[idx] = producto_actualizado
            return producto_actualizado
    return {"mensaje": "Producto no encontrado"}

# Operación para eliminar un producto por ID (DELETE)
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    for idx, prod in enumerate(productos):
        if prod["id"] == producto_id:
            return productos.pop(idx)
    return {"mensaje": "Producto no encontrado"}
