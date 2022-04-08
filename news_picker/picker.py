from . import currency, news, weather


def pick_news():
    weather.make_forecast()
    currency.make_currency()
    news.make_news()
    # TODO other news categories
