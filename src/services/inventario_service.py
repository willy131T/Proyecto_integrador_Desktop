from typing import List, Optional
from config.database import get_db
from src.models.inventario import Inventario

class InventarioService:
    @staticmethod
    def obtener_inventario(categoria: Optional[str] = None, busqueda: Optional[str] = None) -> List[dict]:
        with get_db() as db:
            query = db.query(Inventario)
            if categoria and categoria != "Todas":
                query = query.filter(Inventario.categoria == categoria)
            if busqueda:
                query = query.filter(Inventario.nombre.ilike(f"%{busqueda.strip()}%"))
            materiales = query.order_by(Inventario.categoria.asc(), Inventario.nombre.asc()).all()
            return [
                {
                    "id": m.id,
                    "nombre": m.nombre,
                    "cantidad": m.cantidad,
                    "categoria": m.categoria
                }
                for m in materiales
            ]

    @staticmethod
    def insertar_material(nombre: str, cantidad: int, categoria: str) -> bool:
        with get_db() as db:
            nuevo = Inventario(
                nombre=nombre.strip(),
                cantidad=max(0, cantidad),
                categoria=categoria.strip()
            )
            db.add(nuevo)
            return True

    @staticmethod
    def actualizar_material(id_material: int, nombre: str, cantidad: int, categoria: str) -> bool:
        with get_db() as db:
            item = db.query(Inventario).filter(Inventario.id == id_material).first()
            if not item:
                return False
            item.nombre = nombre.strip()
            item.cantidad = max(0, cantidad)
            item.categoria = categoria.strip()
            return True

    @staticmethod
    def eliminar_material(id_material: int) -> bool:
        with get_db() as db:
            item = db.query(Inventario).filter(Inventario.id == id_material).first()
            if not item:
                return False
            db.delete(item)
            return True

    @staticmethod
    def obtener_alertas_stock_bajo(umbral: int = 15) -> List[dict]:
        with get_db() as db:
            items = db.query(Inventario).filter(Inventario.cantidad <= umbral).all()
            return [
                {"id": i.id, "nombre": i.nombre, "cantidad": i.cantidad, "categoria": i.categoria}
                for i in items
            ]
