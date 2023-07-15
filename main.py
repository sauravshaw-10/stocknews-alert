from datetime import date, timedelta
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

alpha_vantage_api = "73FCNI1U7OJDFAPF"
newsapi_key = "018f1d22f73c470c92a09d0b22d7430d"

api_parameters_alpha = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey" : alpha_vantage_api
}

# Stock Price
response_stk = requests.get(STOCK_ENDPOINT, params=api_parameters_alpha)
response_stk.raise_for_status()
stock_data = response_stk.json()

today = date.today()
yesterday = today - timedelta(days=1)
day_bfr_yest = today - timedelta(days=2)
yesterday = str(yesterday)
day_bfr_yest = str(day_bfr_yest)

yest_close= stock_data["Time Series (Daily)"][yesterday]['4. close']
day_bfr_yest_close = stock_data["Time Series (Daily)"][day_bfr_yest]['4. close']

yest_close = float(yest_close)
day_bfr_yest_close = float(day_bfr_yest_close)
difference = yest_close - day_bfr_yest_close
abs_diff = abs(difference)
per_change = round((abs_diff/day_bfr_yest_close)*100,2)
if difference < 0:
    symbol = "🔻"
else:
    symbol = "🔺"

# Stock News
newsapi_parameters = {
    "q": "tesla",
    # "from": 2023-6-14,
    "sortBy": "popularity",
    "apiKey": newsapi_key,
}

response_news = requests.get(NEWS_ENDPOINT, params=newsapi_parameters)
response_news.raise_for_status()
news_data = response_news.json()

news = news_data["articles"][:3]
titles = [item["title"] for item in news]
descriptions = [item["description"] for item in news]

# SMS alert
api_key = "fe04f499de60c42af83c0381aba63417"
account_sid = "ACe6c45331dcea08d3e7b9c2b803666e9b"
auth_token = "9f59cd5889a6df257c90ffa9d375eeaa"


if per_change >= 5:
    client = Client(account_sid, auth_token)
    message1 = client.messages.create(
        body=f"{STOCK}{symbol}{per_change}%"
             f"\nHeadline: {titles[0]}"
             f"\nBrief: {descriptions[0]}",
        from_='+14027654840',
        to='+919818203823'
    )
    message2 = client.messages \
        .create(
        body=f"{STOCK}{symbol}{per_change}%"
             f"\nHeadline: {titles[1]}"
             f"\nBrief: {descriptions[1]}",
        from_='+14027654840',
        to='+919818203823'
    )
    message3 = client.messages \
        .create(
        body=f"{STOCK}{symbol}{per_change}%"
             f"\nHeadline: {titles[2]}"
             f"\nBrief: {descriptions[2]}",
        from_='+14027654840',
        to='+919818203823'
    )