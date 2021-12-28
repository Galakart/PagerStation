
#TODO фильтрация неподдерживаемых символов, lat-кодировка, транслит в каждой кодировке

dict_symbols_lat = {

}

# слева русские, справа латинские
dict_symbols_cyr = {
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
    'Ю': '\'',
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

dict_symbols_linguist = {
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



class CharsetEncoder():
    def __init__(self):
        pass

    def encode_message(self, message, codepage):
        result = ''
        if codepage == 1:
            pass
        elif codepage == 2:
            result = message
            for cyr_symbol, lat_symbol in dict_symbols_cyr.items():
                result = result.replace(cyr_symbol, lat_symbol)
        elif codepage == 3:
            result = message.upper()
            for cyr_symbol, lat_symbol in dict_symbols_linguist.items():
                result = result.replace(cyr_symbol, lat_symbol)
        return result
