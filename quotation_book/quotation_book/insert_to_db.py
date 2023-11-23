import json
from pathlib import Path
from datetime import datetime

import connect
from models import Author, Quotes


def insert_authors():
    path_to_file = Path(__file__).parent.joinpath("insert_json/authors.json")

    with open(path_to_file, "r", encoding="utf8") as fh:
        file_data = json.load(fh)

    for el in file_data:
        Author(
            fullname=el.get("fullname"),
            born_date=datetime.strptime(el.get("born_date"), "%B %d, %Y"),
            born_location=el.get("born_location"),
            description=el.get("description"),
        ).save()


def insert_quotes():
    path_to_file = Path(__file__).parent.joinpath("insert_json/quotes.json")

    with open(path_to_file, "r", encoding="utf8") as fh:
        file_data = json.load(fh)

    for el in file_data:
        current_name = el.get("author")
        author = Author.objects(fullname=current_name).first()
        Quotes(tags=el.get("tags"), author=author, qoute=el.get("quote")).save()


if __name__ == "__main__":
    insert_authors()
    insert_quotes()
