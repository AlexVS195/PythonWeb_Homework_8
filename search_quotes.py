from models import Quote

def search_quotes(query):
    if query.startswith("name:"):
        author_name = query.split("name:")[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        else:
            print("Author not found.")

    elif query.startswith("tag:"):
        tag = query.split("tag:")[1].strip()
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            print(quote.quote)

    elif query.startswith("tags:"):
        tags = query.split("tags:")[1].strip().split(",")
        quotes = Quote.objects(tags__in=tags)
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