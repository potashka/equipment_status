# status.py
"""
Этот модуль определяет API маршруты для получения состояния оборудования в формате JSON.
"""
import os
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import EquipmentStatus
from app.services import get_equipment_status

router = APIRouter(
    prefix="/status",
    tags=["status"]
)

# Получаем значение GROUP_ID из переменной окружения
group_id_env = os.getenv("GROUP_ID")


@router.get("/data", response_model=list[EquipmentStatus])
def read_status_json(group_id: int = Query(None), db: Session = Depends(get_db)):
    """
    Возвращает состояние оборудования для указанной группы или всего оборудования, если группа не указана.

    Аргументы:
        group_id (int, optional): Идентификатор группы оборудования. Если не указан и не задан в переменной окружения, возвращаются данные для всего оборудования.
        db (Session): Сессия SQLAlchemy для выполнения запроса к базе данных.

    Возвращает:
        list[EquipmentStatus]: JSON список состояния оборудования.
    """
    group_id_to_use = group_id or group_id_env

    result = get_equipment_status(db, group_id_to_use)

    if not result:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return result
