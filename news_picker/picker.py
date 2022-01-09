from . import currency, weather


def pick_news():
    weather.make_forecast()
    currency.make_currency()
    # TODO other news categories
