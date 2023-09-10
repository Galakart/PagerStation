"""Всё по отправке сообщений в эфир"""
from backend.pocsag_ops.charset_encoder import CharsetEncoder
import os



charset_encoder = CharsetEncoder()




def message_to_air(capcode: int, fbit: int, freq: int, baudrate: int, id_codepage: int, message: str) -> bool:
    """Отправляет сообщение в эфир

    Args:
        capcode (int): капкод
        fbit (int): id источника
        freq (int): частота в Гц
        baudrate (int): id скорости
        id_codepage (int): id кодировки текста
        message (str): сообщение

    Returns:
        bool: успех
    """
    capcode = f'{capcode:07d}'
    message_text = charset_encoder.encode_message(message, id_codepage)
    if not os.path.exists('./pocsag'):
        return False
    os.system(f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -r {baudrate} -t 1')
    return True
