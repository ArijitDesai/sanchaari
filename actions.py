import httpx
import math
import os

def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

def calculate(what):
    try:
        return str(eval(what, {"__builtins__": None}, {"math": math}))
    except Exception as e:
        return str(e)

def current_time(place):
    try:
        response = httpx.get(f"http://worldtimeapi.org/api/timezone/{place}")
        if response.status_code == 200:
            data = response.json()
            return data['datetime']
        else:
            return f"Could not retrieve time for {place}. Please ensure the place is specified in 'Area/Location' format (e.g., 'America/New_York')."
    except Exception as e:
        return str(e)

def dictionary(word):
    try:
        response = httpx.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return f"The definition of {word} is: {definition}"
        else:
            return f"Could not find the definition for {word}."
    except Exception as e:
        return str(e)

def news(topic):
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    try:
        response = httpx.get(f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}")
        if response.status_code == 200:
            articles = response.json()['articles']
            headlines = [article['title'] for article in articles[:5]]
            return f"Top headlines for {topic}: " + "; ".join(headlines)
        else:
            return f"Could not retrieve news for {topic}. Please check the topic name."
    except Exception as e:
        return str(e)

def stock_price(company):
    STOCKS_API_KEY = os.getenv('STOCKS_API_KEY')
    try:
        print(f"https://finnhub.io/api/v1/quote?symbol={company}&token={STOCKS_API_KEY}")
        response = httpx.get(f"https://finnhub.io/api/v1/quote?symbol={company}&token={STOCKS_API_KEY}")
        if response.status_code == 200:
            data = response.json()
            current_price = data['c']
            return f"The current stock price of {company} is ${current_price}."
        else:
            return f"Could not retrieve stock price for {company}. Please check the company symbol."
    except Exception as e:
        return str(e)

def translate(text, target_language):
    try:
        response = httpx.get(f"https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_language}")
        if response.status_code == 200:
            translation = response.json()['responseData']['translatedText']
            return f"The translation of '{text}' in {target_language} is: {translation}"
        else:
            return f"Could not translate text. Please check the text and target language."
    except Exception as e:
        return str(e)

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "current_time": current_time,
    "dictionary": dictionary,
    "news": news,
    "stock_price": stock_price,
    "translate": translate
}
