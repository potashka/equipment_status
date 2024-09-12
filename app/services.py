# services.py
"""
Этот модуль содержит бизнес-логику для API состояния оборудования.
Функции:
    get_equipment_status: Получает состояние оборудования для определенной группы
    или всего оборудования.
"""
from sqlalchemy.orm import Session


def get_equipment_status(db: Session, group_id: int = None):
    """
    Получает состояние оборудования для указанной группы или всего оборудования из базы данных.

    Аргументы:
        db (Session): Сессия SQLAlchemy для выполнения запроса к базе данных.
        group_id (int, optional): Идентификатор группы оборудования.
        Если None, возвращаются данные для всего оборудования.
    Возвращает:
        list: Список кортежей, представляющих состояние оборудования.
    """
    query = """
    WITH active_channels AS (
        SELECT
            ec.equipment_id,
            ec.channel_id,
            ec.sens_level
        FROM
            equipment_channels ec
        WHERE
            ec.is_active = TRUE
    ),
    last_minute_data AS (
        SELECT
            md.equipment_id,
            md.channel_id,
            md.avg_val,
            md.moment
        FROM
            minuted_data md
        WHERE
            md.moment >= NOW() - INTERVAL '15 minutes'
    )
    SELECT
        e.equipment_id,
        e.equipment_name,
        CASE
            WHEN e.equipment_status = 2 THEN 'repair'
            WHEN e.equipment_status = 1 AND EXISTS (
                SELECT 1
                FROM active_channels ac
                JOIN last_minute_data lmd ON ac.equipment_id = lmd.equipment_id AND ac.channel_id = lmd.channel_id
                WHERE lmd.avg_val > ac.sens_level
            ) THEN 'working'
            WHEN e.equipment_status = 1 THEN 'idle'
            ELSE 'unknown'
        END AS status
    FROM
        equipment e
    """
    
    if group_id is not None:
        query += "WHERE e.group_id = :group_id"
        result = db.execute(query, {"group_id": group_id}).fetchall()
    else:
        result = db.execute(query).fetchall()

    return result
