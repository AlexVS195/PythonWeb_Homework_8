import json
from mongoengine import connect
from models import Author, Quote

# Підключення до бази даних Atlas MongoDB
connect("myFirstDatabase",
        host="mongodb+srv://osymashk:Langeron2024!@cluster0.oepyyjj.mongodb.net/",
        retryWrites=True,
        w="majority",
        appName="Cluster0")

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

print("Дані авторів були успішно завантажені в базу даних.")

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

print("Дані цитат були успішно завантажені в базу даних.")