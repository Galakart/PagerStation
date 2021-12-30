"""Расчёт фрейма у капкода"""
import sys


def calculate_frame(capcode):
    print(f'Frame: {capcode % 8}')


if __name__ == '__main__':
    try:
        cap = int(sys.argv[1])
        if cap < 0 or cap > 9999999:
            raise ValueError
    except ValueError:
        print('Wrong capcode')
        sys.exit()

    calculate_frame(cap)
