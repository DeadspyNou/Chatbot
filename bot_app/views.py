from django.http import JsonResponse
from django.shortcuts import render
import re
import requests, json
from bs4 import BeautifulSoup
from datetime import datetime
import random
from googletrans import Translator
import wikipedia
from PyDictionary import PyDictionary 

def index(request):
    return render(request, 'index.html', {'name': 'ChatBot'})

def ajax_part(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        user_message = request.GET.get('textData', '').lower().strip()
        print(user_message)
        BOTMSG = process_message(user_message)
        return JsonResponse({'BOTMSG': BOTMSG})

def process_message(message):
    if message in ['hey', 'hello', 'hi', 'hii', 'hiii']:
        return f"{message} Its deadspy's_BOT\nType Query for More Info"

    if message in ['query', 'queries']:
        return get_query_syntax()

    if 'toss a coin' in message:
        return f"ITS AN {random.choice(['HEADS', 'TAILS'])}."

    if 'roll a die' in message:
        return f"The Upper Face is {random.choice(['1', '2', '3', '4', '5', '6'])}."

    if 'translate' in message:
        return handle_translation(message)

    if 'wikipedia' in message:
        return search_wikipedia(message)

    if 'meaning' in message:
        return get_word_meaning(message)

    if 'weather in' in message:
        return get_weather_info(message)

    if 'insta of' in message:
        return get_instagram_info(message)

    if 'date' in message:
        return datetime.now().strftime("Local Date\n%A %B\n\t%d/%m/%Y")

    if 'time' in message:
        return datetime.now().strftime("Local Time\n%H:%M %p")

    if 'news' in message:
        return get_news()

    if 'corona stats in' in message:
        return get_corona_stats(message)

    if 'quote' in message:
        return get_random_quote()

    if 'calculate' in message:
        return calculate_expression(message)

    if 'multiplication table' in message:
        return generate_multiplication_table(message)

    if 'binary' in message:
        return string_to_binary(message)

    if 'reverse' in message:
        return reverse_string(message)

    if 'string' in message:
        return binary_to_string(message)

    return "Sorry, I didn't understand that. Type 'query' for options."


def get_query_syntax():
    return (
        "~ ~ Querys ~ ~\n1) Weather : weather in {city name}\n2) INSTA : insta of {Username}\n"
        "3) DATE : date\n4) TIME : time\n5) NEWS : news\n6) CORONA STATISTICS : corona stats in {Country}\n"
        "7) QUOTES : quote\n8) CONVERT-TO-BINARY : binary {string}\n9) CONVERT-TO-STRING : string {binary}\n"
        "10) REVERSE : reverse {string}\n11) MULTIPLICATION TABLE : multiplication table of {No}\n"
        "12) CALCULATE : calculate {equation}\n13) COIN TOSS : toss a coin\n14) ROLL DIE : roll a die\n"
        "15) Translate : translate from {LANGUAGE} to {LANGUAGE} {SENTENCE}\n16) MEANING : meaning of {WORD}\n"
        "17) Wikipedia : wikipedia {Search}"
    )

def handle_translation(message):
    try:
        from_lang, to_lang, text = re.findall(r'translate from (\w+) to (\w+) (.+)', message)[0]
        translator = Translator()
        translated = translator.translate(text, src=from_lang, dest=to_lang)

        return translated.text  
    except Exception as e:
        return f"Error: {str(e)}\nQuery ALERT: translate from {{LANGUAGE}} to {{LANGUAGE}} {{THE SENTENCE}}"

def search_wikipedia(message):
    try:
        search_term = re.findall(r'wikipedia (.+)', message)[0]
        return wikipedia.summary(search_term, sentences=2)
    except:
        return "Can't Find Anything"

def get_word_meaning(message):
    try:
        word = re.findall(r'meaning of (.+)', message)[0]
        dictionary = PyDictionary()
        return str(dictionary.meaning(word))
    except:
        return 'Not Found Any Meaning Of The Word'

def get_weather_info(message):
    try:
        city_name = re.findall(r'weather in (.+)', message)[0]
        api_key = "your_api_key_here"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        response = requests.get(url).json()
        if response.get("cod") != "404":
            main = response["main"]
            weather_desc = response["weather"][0]["description"]
            return (
                f"WEATHER INFORMATION\nCity: {city_name.upper()}\n"
                f"Temperature: {main['temp']}K\nPressure: {main['pressure']} hPa\n"
                f"Humidity: {main['humidity']}%\nDescription: {weather_desc}"
            )
        return "CITY NOT FOUND OR NOT CONNECTED TO THE INTERNET"
    except:
        return "API has been shutdown."

def get_instagram_info(message):
    try:
        username = re.findall(r'insta of (.+)', message)[0]
        url = f"https://www.instagram.com/{username}/"
        response = requests.get(url)
        if response.status_code != 200:
            return "Failed to retrieve Instagram profile. Please check the username."
        soup = BeautifulSoup(response.text, "html.parser")
        meta = soup.find("meta", property="og:description")
        if meta and meta.get('content'):
            details = meta['content'].split(' - ')[0].split(' ')
            followers = details[0]
            following = details[2]
            posts = details[4]
            return (f"INSTA PROFILE DETAILS\n"
                    f"USERNAME: {username}\n"
                    f"FOLLOWERS: {followers}\n"
                    f"FOLLOWING: {following}\n"
                    f"POSTS: {posts}")
        else:
            return "Could not find profile details. Instagram may have updated its layout."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_news():
    try:
        response = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=367cd90c0f664280a6c5614009e680d9')
        if response.status_code == 200:
            articles = response.json()['articles'][:5]
            news_items = [
                f"<strong>{article['title']}</strong><br>"
                f"<a href='{article['url']}' target='_blank'>Read more</a>"
                for article in articles
            ]
            return '<br><br>'.join(news_items) 
        return 'Unable to fetch news at this time.'
    except Exception:
        return "Can't connect to the Internet"

def get_corona_stats(message):
    try:
        country = re.findall(r'corona stats in (.+)', message)[0]
        response = requests.get('https://api.apify.com/v2/actor-tasks/5MjRnMQJNMQ8TybLD/runs/last/dataset/items')
        if response.status_code == 200:
            country_data = [data for data in response.json() if data['country'].lower() == country.lower()]
            if country_data:
                data = country_data[0]
                last_updated = datetime.strptime(data['lastUpdatedApify'], "%Y-%m-%dT%H:%M:%S.%fZ")
                return (
                    f"Corona Status\nCountry: {data['country']}\nInfected: {data['infected']}\n"
                    f"Tested: {data['tested']}\nRecovered: {data['recovered']}\nDeceased: {data['deceased']}\n"
                    f"Last updated: {last_updated.strftime('%d/%m/%Y %H:%M:%S')} UTC"
                )
            return "No data found for the specified country."
        return "API has been shutdown."
    except:
        return "An error occurred while fetching corona statistics."

def get_random_quote():
    quotes = [
        "The best way to predict the future is to create it.",
        "Life is what happens when you're busy making other plans.",
        "You only live once, but if you do it right, once is enough.",
        "The purpose of our lives is to be happy.",
        "Get busy living or get busy dying."
    ]
    return random.choice(quotes)

def calculate_expression(message):
    try:
        equation = re.findall(r'calculate (.+)', message)[0]
        return f"The result is: {eval(equation)}"
    except:
        return "Invalid calculation. Please try again with a valid equation."

def generate_multiplication_table(message):
    try:
        
        match = re.findall(r'multiplication table of (\d+) till (\d+)', message)
        if match:
            number, times = map(int, match[0])
        else:
            match = re.findall(r'multiplication table of (\d+)', message)
            if match:
                number = int(match[0])
                times = 10  
            else:
                return "Invalid input format. Please specify like 'multiplication table of 5 till 10'."
        
        
        return '\n'.join([f"{number} x {i} = {number * i}" for i in range(1, times + 1)])
    except (ValueError, IndexError):
        return "Invalid input for multiplication table."

def string_to_binary(message):
    try:
        text = re.findall(r'binary (.+)', message)[0]
        return ' '.join(format(ord(char), '08b') for char in text)
    except:
        return "Error converting string to binary."

def reverse_string(message):
    try:
        text = re.findall(r'reverse (.+)', message)[0]
        return text[::-1]
    except:
        return "Error reversing string."

def binary_to_string(message):
    try:
        binary_input = re.findall(r'string (.+)', message)[0]
        ascii_values = [int(b, 2) for b in binary_input.split()]
        return ''.join(chr(i) for i in ascii_values)
    except:
        return "Error converting binary to string."
