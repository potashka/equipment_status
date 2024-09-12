# main.py
"""
Основной файл приложения FastAPI для отображения дашборда состояния оборудования.
"""

import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers import status

app = FastAPI()

# Подключение статики (CSS) и шаблонов (HTML)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Подключение маршрутов из status.py
app.include_router(status.router)

# Получаем значение GROUP_ID из переменной окружения
group_id = os.getenv("GROUP_ID")


@app.get("/")
def render_dashboard(request: Request):
    """
    Рендерит HTML-дашборд для отображения состояния оборудования.

    Аргументы:
        request (Request): Объект запроса.

    Возвращает:
        TemplateResponse: HTML-шаблон дашборда.
    """
    return templates.TemplateResponse("dashboard.html", {"request": request, "group_id": group_id})
