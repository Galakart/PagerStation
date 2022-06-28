"""Расчёт фрейма у капкода"""
import sys


def calculate_frame(cap_number):
    print(f'Frame: {cap_number % 8}')


if __name__ == '__main__':
    try:
        capcode = int(sys.argv[1])
        if capcode < 0 or capcode > 9999999:
            raise ValueError
    except ValueError:
        print('Wrong capcode')
        sys.exit()

    calculate_frame(capcode)
