> [!NOTE]
> You need to have a twilio account and a virutal number from the API in order to run this program, otherwise it will not work as you will not be able to send the SMS to your phone.
> You are also able to run this program using the Pythonanywhere hosting service for free (https://www.pythonanywhere.com/).


This is one interesting program. I used 3 APIs to make the whole thing work. This project basically notifies you throught SMS if a specified stock has increased or decreased a specific % in the last 24h.
Alphavantage API (https://www.alphavantage.co/query) is used to gatherr the stock market information to compare the closing amount from yesterday and the day before yesterday.
Newsapi APIs (https://newsapi.org/v2/everything) is used to gather the most recent articles from the company of the stock we're trying to investigate.
Last but not least we use Twilio's API (https://www.twilio.com/en-us) to send all thuis information to our phone.
