import random
import requests

# Dictionary of possible default responses
# Scalability is possible with implementation like natural language processing
responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "how are you": ["I'm doing well, thank you", "I'm great! How about you?"],
    "food": ["I like pizza!", "Maybe double cheeseburger", "Some nigiri sushi?", "Chinese food!"],
    "weather": [],
    "news": [],
    "roll a die": ["1", "2", "3", "4", "5", "6"],
    "flip a coin": ["It's heads.", "It's tails."]
}

# Function that generates random responses
def get_response(message):
    if "weather" in message.lower():
        location = input("Chatbot: Which city would you like the weather for? ")
        return get_weather_data(location)
    elif "news" in message.lower():
        keyword = input("Chatbot: What kind of news are you interested in? ")
        articles = get_news(keyword)
        if len(articles) > 0:
            news = f"Here are the top news articles about {keyword}: "
            for article in articles:
                news += f"\n\n{article['title']}\n{article['url']}"
        else:
            news = f"Sorry, no news articles were found for {keyword}. "
        return news
    elif message.lower() in responses:
        return random.choice(responses[message.lower()])
    else:
        return "I'm sorry I didn't understand, I'm still learning."

# Function that grabs weather data from OpenWeatherMapAPI
def get_weather_data(location):
    api_key = "bf794cb4c2b3f8bbedc18aed543f0daa"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    weather_response = requests.get(url)
    if weather_response.status_code == 200:
        data = weather_response.json()
        temp_celsius = round(data['main']['temp'] - 273.15, 1)
        temp = round(temp_celsius * 1.8 + 32, 1)
        desc = data['weather'][0]['description']
        return f"The current weather in {location.title()} is {temp}F and {desc}."
    else:
        return "Sorry, I could not retrieve the weather data at this time."

# Function that grabs news from NewsAPI.org
def get_news(keyword):
    api_key = "b908e3bfd09540199765147fc89e755a"
    url = f"https://newsapi.org/v2/top-headlines?q={keyword}&apiKey={api_key}"
    news_response = requests.get(url)
    articles = []
    if news_response.status_code == 200:
        data = news_response.json()
        articles = data["articles"]
        return articles
    else:
        return "Sorry, I could not retrieve the news data this time. "
# The bot
while True:
    message = input("You: ")
    if message.lower() == "bye":
        print("Chatbot: Good day to you!")
        break
    response = get_response(message)
    print("Chatbot: ", response)

