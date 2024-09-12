# models.py
"""
Этот модуль содержит модели Pydantic для валидации и сериализации данных.
Модели:
    EquipmentStatus: Представляет состояние оборудования.
"""
from pydantic import BaseModel


class EquipmentStatus(BaseModel):
    """
    Модель Pydantic, представляющая состояние оборудования.
    Атрибуты:
        equipment_id (int): Уникальный идентификатор оборудования.
        equipment_name (str): Название оборудования.
        status (str): Текущее состояние оборудования (например, 'repair', 'working', 'idle').
    """
    equipment_id: int
    equipment_name: str
    status: str
