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

# Получаем значение GROUP_ID из переменной окружения и преобразуем в целое число
group_id_env = os.getenv("GROUP_ID")
if group_id_env is not None:
    try:
        group_id_env = int(group_id_env)
    except ValueError:
        raise ValueError(f"Invalid GROUP_ID environment variable: {group_id_env}")


@router.get("/data", response_model=dict)
def read_status_json(group_id: int = Query(None), db: Session = Depends(get_db)):
    """
    Возвращает состояние оборудования для указанной группы или всего оборудования, если группа не указана.

    Аргументы:
        group_id (int, optional): Идентификатор группы оборудования. Если не указан и не задан в переменной окружения, возвращаются данные для всего оборудования.
        db (Session): Сессия SQLAlchemy для выполнения запроса к базе данных.

    Возвращает:
        dict: JSON с названием цеха и списком состояния оборудования.
    """
    # Используем переданный group_id или значение из переменной окружения
    group_id_to_use = group_id if group_id is not None else group_id_env

    # Проверяем, что group_id_to_use имеет тип int или None
    if group_id_to_use is not None and not isinstance(group_id_to_use, int):
        try:
            group_id_to_use = int(group_id_to_use)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid group_id format")

    # Отладочный вывод для проверки значения group_id_to_use
    print(f"Using group_id: {group_id_to_use}")

    equipment_list = get_equipment_status(db, group_id_to_use)

    if not equipment_list:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # Предполагаем, что все элементы имеют одинаковый group_name
    group_name = equipment_list[0]["group_name"] if equipment_list[0]["group_name"] else "Все цеха"

    return {
        "group_name": group_name,
        "equipment": equipment_list
    }
