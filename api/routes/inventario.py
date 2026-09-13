from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.services.inventario_service import InventarioService

router = APIRouter(prefix="/api/inventario", tags=["Inventario"])

class MaterialDTO(BaseModel):
    nombre: str = Field(..., min_length=2)
    cantidad: int = Field(..., ge=0)
    categoria: str = Field(default="Materiales")

@router.get("")
def listar_inventario(categoria: Optional[str] = None, buscar: Optional[str] = None):
    items = InventarioService.obtener_inventario(categoria=categoria, busqueda=buscar)
    return {"inventario": items}

@router.get("/alertas")
def obtener_alertas_stock(umbral: int = 15):
    alertas = InventarioService.obtener_alertas_stock_bajo(umbral)
    return {"alertas": alertas}

@router.post("")
def agregar_material(data: MaterialDTO):
    ok = InventarioService.insertar_material(data.nombre, data.cantidad, data.categoria)
    if not ok:
        raise HTTPException(status_code=400, detail="Error al agregar insumo")
    return {"success": True, "mensaje": "Insumo registrado correctamente"}

@router.put("/{id_material}")
def actualizar_material(id_material: int, data: MaterialDTO):
    ok = InventarioService.actualizar_material(id_material, data.nombre, data.cantidad, data.categoria)
    if not ok:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return {"success": True, "mensaje": "Insumo actualizado exitosamente"}

@router.delete("/{id_material}")
def eliminar_material(id_material: int):
    ok = InventarioService.eliminar_material(id_material)
    if not ok:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    return {"success": True, "mensaje": "Insumo eliminado exitosamente"}