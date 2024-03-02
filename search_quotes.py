import json
from mongoengine import connect
from models import Author, Quote

# Підключення до бази даних MongoDB
connect("myFirstDatabase",
        host="mongodb+srv://osymashk:Langeron2024!@cluster0.oepyyjj.mongodb.net/",
        retryWrites=True,
        w="majority",
        appName="Cluster0")

def search_quotes(query):
    query = query.lower()  # Перетворення команди на нижній регістр
    if query.startswith("name:"):
        author_name = query.split("name:")[1].strip()
        author = Author.objects(fullname__iexact=author_name).first()  # Пошук автора без урахування регістру
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        else:
            print("Author not found.")

    elif query.startswith("tag:"):
        tag = query.split("tag:")[1].strip()
        quotes = Quote.objects(tags__icontains=tag)  # Пошук за тегом без урахування регістру
        for quote in quotes:
            print(quote.quote)

    elif query.startswith("tags:"):
        tags = query.split("tags:")[1].strip().split(",")
        quotes = Quote.objects(tags__in=[tag.strip().lower() for tag in tags])  # Пошук за тегами без урахування регістру
        for quote in quotes:
            print(quote.quote)

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
