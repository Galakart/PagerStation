import datetime

from fastapi import APIRouter, Form, Path, Request
from fastapi.responses import FileResponse, HTMLResponse

import db

router = APIRouter()


@router.get("/capcode_to_frame/{capcode}")
def capcode_to_frame(capcode: int = Path(ge=1, le=9999999)):
    return {"frame_number": capcode % 8}


@router.get("/to_admin", response_class=FileResponse)
def msg_for_admin_form():
    return "templates/to_admin.html"


@router.post("/to_admin_form_action", response_class=HTMLResponse)
def to_admin_form_action(request: Request, mes_text=Form()):
    client_ip = request.client.host
    if not mes_text:
        return """
            <CENTER>
                <p><b>Введите сообщение!!!</b></p>
                <a href="./to_admin">назад</a>
            </CENTER>
            """

    stricts_ipaddress_item = db.db_messages.get_stricts_ipaddress(client_ip)
    if stricts_ipaddress_item and stricts_ipaddress_item.last_send > datetime.datetime.now() - datetime.timedelta(minutes=1):
        return """
            <CENTER>
                <p><b>Установлено ограничение на 1 сообщение в минуту</b></p>
                <a href="./to_admin">назад</a>
            </CENTER>
            """

    admins_tuple = db.db_users.get_admins()
    if admins_tuple:
        for admin_item in admins_tuple:
            pagers = db.db_users.get_user_pagers(admin_item.id)
            for pager_item in pagers:
                db.db_messages.create_message_private(pager_item.id, mes_text)
    else:
        return """
            <CENTER>
                <p><b>Админов в сервисе не зарегистрировано</b></p>
                <a href="./to_admin">назад</a>
            </CENTER>
            """

    db.db_messages.create_or_update_stricts_ipaddress(client_ip)
    return """
            <CENTER>
                <p><b>Сообщение отправлено</b></p>
                <a href="./to_admin">назад</a>
            </CENTER>
            """
