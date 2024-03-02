import json
from mongoengine import connect
from models import Author, Quote
import redis
import re

# Підключення до бази даних Atlas MongoDB
connect("myFirstDatabase",
        host="mongodb+srv://osymashk:Langeron2024!@cluster0.oepyyjj.mongodb.net/",
        retryWrites=True,
        w="majority",
        appName="Cluster0")

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
# Функція для кешування результату
def cache_result(key, value):
    redis_client.set(key, json.dumps(value))

# Функція для отримання результату з кешу
def get_cached_result(key):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

# Завантаження даних з файлу authors.json
with open("C:/Users/AlexPC/Repository/PythonWeb/Homework_8/authors.json", "r", encoding="utf-8") as file:
    authors_data = json.load(file)
    for author_data in authors_data:
        author = Author(
            fullname=author_data["fullname"],
            born_date=author_data["born_date"],
            born_location=author_data["born_location"],
            description=author_data["description"]
        )
        author.save()

# Завантаження даних з файлу quotes.json
with open("C:/Users/AlexPC/Repository/PythonWeb/Homework_8/quotes.json", "r", encoding="utf-8") as file:
    quotes_data = json.load(file)
    for quote_data in quotes_data:
        author = Author.objects(fullname=quote_data["author"]).first()
        if author:
            quote = Quote(
                tags=quote_data["tags"],
                author=author,
                quote=quote_data["quote"]
            )
            quote.save()

# Функція для пошуку цитат з кешуванням
def search_quotes(query):
    cached_result = get_cached_result(query)
    if cached_result:
        for quote in cached_result:
            print(quote)
        return

    if query.startswith("name:") or query.startswith("tag:"):
        # Заміна скороченого запису на повний формат
        query = re.sub(r'^name:st', 'name:Steve Martin', query)
        query = re.sub(r'^tag:li', 'tag:life', query)

    if query.startswith("name:"):
        author_name = query.split("name:")[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            result_quotes = [quote.quote for quote in quotes]
            cache_result(query, result_quotes)
            for quote in result_quotes:
                print(quote)
        else:
            print("Author not found.")

    elif query.startswith("tag:"):
        tag = query.split("tag:")[1].strip()
        quotes = Quote.objects(tags=tag)
        result_quotes = [quote.quote for quote in quotes]
        cache_result(query, result_quotes)
        for quote in result_quotes:
            print(quote)

    elif query.startswith("tags:"):
        tags = query.split("tags:")[1].strip().split(",")
        quotes = Quote.objects(tags__in=tags)
        result_quotes = [quote.quote for quote in quotes]
        cache_result(query, result_quotes)
        for quote in result_quotes:
            print(quote)

    elif query == "exit":
        return False

    else:
        print("Invalid command.")

    return True

# Головний цикл програми
while True:
    user_input = input("Enter command: ")
    if not search_quotes(user_input):
        break