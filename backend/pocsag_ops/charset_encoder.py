"""Кодировка символов для пейджера"""
from transliterate import translit
from transliterate.base import TranslitLanguagePack, registry
from transliterate.discover import autodiscover

from backend.models.model_hardware import CodepageEnum

ALLOWED_SYMBOLS = [
    ' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
    '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
    '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
]

SYMBOLS_CYR = {
    'А': 'a',
    'Б': 'b',
    'В': 'w',
    'Г': 'g',
    'Д': 'd',
    'Е': 'e',
    'Ё': 'e',
    'Ж': 'v',
    'З': 'z',
    'И': 'i',
    'Й': 'j',
    'К': 'k',
    'Л': 'l',
    'М': 'm',
    'Н': 'n',
    'О': 'o',
    'П': 'p',
    'Р': 'r',
    'С': 's',
    'Т': 't',
    'У': 'u',
    'Ф': 'f',
    'Х': 'h',
    'Ц': 'c',
    'Ч': '~',
    'Ш': '{',
    'Щ': '}',
    'Ъ': 'x',
    'Ы': 'y',
    'Ь': 'x',
    'Э': '|',
    'Ю': '\`',
    'Я': 'q',
    'а': 'A',
    'б': 'B',
    'в': 'W',
    'г': 'G',
    'д': 'D',
    'е': 'E',
    'ё': 'E',
    'ж': 'V',
    'з': 'Z',
    'и': 'I',
    'й': 'J',
    'к': 'K',
    'л': 'L',
    'м': 'M',
    'н': 'N',
    'о': 'O',
    'п': 'P',
    'р': 'R',
    'с': 'S',
    'т': 'T',
    'у': 'U',
    'ф': 'F',
    'х': 'H',
    'ц': 'C',
    'ч': '^',
    'ш': '[',
    'щ': ']',
    'ъ': 'X',
    'ы': 'Y',
    'ь': 'X',
    'э': '\\',
    'ю': '@',
    'я': 'Q',
}

SYMBOLS_LINGUIST = {
    'А': 'A',
    'Б': 'a',
    'В': 'B',
    'Г': 'b',
    'Д': 'd',
    'Е': 'E',
    'Ё': 'e',
    'Ж': 'f',
    'З': 'g',
    'И': 'h',
    'Й': 'i',
    'К': 'K',
    'Л': 'j',
    'М': 'M',
    'Н': 'H',
    'О': 'O',
    'П': 'k',
    'Р': 'P',
    'С': 'C',
    'Т': 'T',
    'У': 'l',
    'Ф': 'm',
    'Х': 'X',
    'Ц': 'n',
    'Ч': 'o',
    'Ш': 'p',
    'Щ': 'q',
    'Ъ': 'r',
    'Ы': 's',
    'Ь': 't',
    'Э': 'u',
    'Ю': 'v',
    'Я': 'w',
}


class RuExtendedLanguagePack(TranslitLanguagePack):
    language_code = "ru_ext"
    language_name = "RU Extended"

    mapping = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "абкдефгхийклмнопqрстуввxызАБКДЕФГХИЙКЛМНОПQРСТУВВXЫЗ",
    )

    pre_processor_mapping = {
        "the": "зе", "The": "Зе", "THE": "ЗЕ",
        "ech": "ех", "Ech": "Ех", "ECH": "ЕХ",
        "chr": "хр", "Chr": "Хр", "CHR": "ХР",
        "you": "ю", "You": "Ю", "YOU": "Ю",

        "ch": "ч", "Ch": "Ч", "CH": "Ч",
        "gy": "джи", "Gy": "Джи", "GY": "ДЖИ",

        "q": "ку", "Q": "Ку",
        "x": "кс", "X": "КС",
    }


class CharsetEncoder():
    def __init__(self):
        autodiscover()
        registry.register(RuExtendedLanguagePack)

    def encode_message(self, message, id_codepage):
        message = message \
            .replace('«', '"') \
            .replace('»', '"') \
            .replace('&amp;', '&') \
            .replace('&gt;', '>') \
            .replace('&lt;', '<') \
            .replace('&quot;', '"')

        # в эфир передаются только латинские буквы и спецсимволы (то есть по сути, весь набор lat),
        # так что так или иначе, независимо от заданной кодировки, нам нужно преобразовать её в набор lat
        result = ''
        if id_codepage == CodepageEnum.LAT.value:
            # набор уже lat, ничего преобразовывать не нужно, только если встречаются русские символы,
            # то транслитерируем их в латиницу. В конце проверим, не затесались ли символы, которых нету в наборе
            lat_text = translit(message, 'ru_ext', reversed=True)
            result = self.check_allowed_symbols(lat_text)

        elif id_codepage == CodepageEnum.CYR.value:
            # переведём все английские слова в русский транслит (так как из-за сопоставления таблиц перекодировок идёт
            # смена регистра, чтобы потом не наблюдать на пейджере что-то вроде тЕЦХНОЛОГЫ),
            # затем перекодируем в lat по словарю SYMBOLS_CYR
            ru_text = translit(message, 'ru_ext')
            for cyr_symbol, lat_symbol in SYMBOLS_CYR.items():
                ru_text = ru_text.replace(cyr_symbol, lat_symbol)
            result = self.check_allowed_symbols(ru_text)

        elif id_codepage == CodepageEnum.LINGUIST.value:
            # Транслитерация не нужна, но в этом наборе только заглавные буквы, так что сделаем их такими,
            # и потом уже кодируем встречающиеся русские заглавные символы по словарю SYMBOLS_LINGUIST.
            # Встречающиеся латинские заглавные кодировать не нужно, они совпадают с набором lat
            linguist_text = message.upper()
            for cyr_symbol, lat_symbol in SYMBOLS_LINGUIST.items():
                linguist_text = linguist_text.replace(cyr_symbol, lat_symbol)
            result = self.check_allowed_symbols(linguist_text)

        return result

    def check_allowed_symbols(self, mes_text: str) -> str:
        mes_lst = list(mes_text)
        for mes_symbol in mes_lst:
            if mes_symbol not in ALLOWED_SYMBOLS:
                mes_text = mes_text.replace(mes_symbol, '')
        return mes_text
