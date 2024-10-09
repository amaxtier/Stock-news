from dotenv import load_dotenv
import os
import datetime as dt
import requests
from twilio.rest import Client

# functions
def percentage(part:float, whole:float) -> float:
    return (part/whole * 100) - 100
    
# Time
now = dt.datetime.now()
yesterday = str(now - dt.timedelta(days=1)).split()[0]
day_before_yesterday = str(now - dt.timedelta(days=2)).split()[0]

# Stock
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

load_dotenv(dotenv_path='.env')

# Alpha
alpha_vantage_api_key = os.getenv('ALPHA_KEY')
APLHA_VANTAGE_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": alpha_vantage_api_key,
}

APLHA_VANTAGE_RESPONSE = requests.get(
    url="https://www.alphavantage.co/query", 
    params=APLHA_VANTAGE_PARAMETERS
)

APLHA_VANTAGE_RESPONSE.raise_for_status()
print(APLHA_VANTAGE_RESPONSE.status_code)
stock_data = APLHA_VANTAGE_RESPONSE.json()["Time Series (Daily)"]

# Stock Variables
stock_data_yesterday_close = round(float(stock_data[yesterday]["4. close"]))
stock_data_day_before_yesterday_close = round(float(stock_data[day_before_yesterday]["4. close"]))

# Process
if percentage(5, 100) >= 5 or percentage(stock_data_yesterday_close, stock_data_day_before_yesterday_close) <= 5: 
    NEWS_API_KEY = os.getenv('NEWS_KEY')
    NEWS_API_PARAMETERS = {
    "q": COMPANY_NAME,
    "from": yesterday,
    "sortBy":"publishedAt",
    "apiKey": NEWS_API_KEY,
    } 
    
    NEWS_API_RESPONSE = requests.get(
    url="https://newsapi.org/v2/everything", 
    params=NEWS_API_PARAMETERS
    )
    NEWS_API_RESPONSE.raise_for_status()
    print(NEWS_API_RESPONSE.status_code)
    news_data = NEWS_API_RESPONSE.json()["articles"][0:3]
    
    account_sid = os.getenv('CLIENT_ID')
    auth_token = os.getenv('CLIENT_SECRET')
    client = Client(account_sid, auth_token)
    
    for news in news_data:
        message = client.messages.create(
            body=f"{STOCK}: 🔺{percentage(stock_data_yesterday_close,stock_data_day_before_yesterday_close)}\n\nHeadline: {news['title']}\n\nBrief: {news['description']}\n\n{news['url']}",
            from_='+18508208159',
            to= os.getenv('NUMBER')
            )