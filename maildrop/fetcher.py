from maildrop import md_currency, md_weather


def pull_data():
    md_weather.make_forecast()
    md_currency.make_currency()
