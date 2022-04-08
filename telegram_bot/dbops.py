import datetime

# from rest_backend.models import Pager, PrivateMessage


def send_ping_private():
    cur_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    # pager = Pager.objects.get(subscriber_number=1111)
    # mes = f'Пинг! {cur_time}'
    # PrivateMessage(pager=pager, message=mes).save()
    return True
