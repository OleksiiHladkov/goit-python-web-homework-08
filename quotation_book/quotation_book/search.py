from models import Author, Quotes
import connect


def parcing_data(data: str):
    result = {}

    data_list = data.split(":")

    if len(data_list):
        result["command"] = data_list[0]
        if len(data_list) > 1:
            result["value"] = data_list[1].strip().split(",")

    return result


def process_objects(objects: list) -> str:
    result = []

    for object in objects:
        author_fullname = object.author.fullname
        quote_dict = object.to_mongo().to_dict()
        tags = ", ".join(quote_dict.get("tags"))
        quote = quote_dict.get("qoute")
        result.append(f"\nAuthor: {author_fullname}\nTags: {tags}\nQoute: {quote}\n")

    return "\n".join(result)


def input_error(handler_func):
    def inner_func(**kwargs):
        try:
            result = handler_func(**kwargs)
        except KeyError as key:
            result = f"Search is not possible: {key} is not found"
        except IndexError:
            result = f"Values sequence index out of range"

        return result

    return inner_func


@input_error
def search_by_name(**kwargs):
    fullname = kwargs["value"][0]
    author = Author.objects(fullname=fullname).first()
    quotes = Quotes.objects(author=author)
    result = process_objects(quotes)
    return result


@input_error
def search_by_names(**kwargs):
    fullnames = kwargs["value"]
    authors = Author.objects(fullname__in=fullnames)
    quotes = Quotes.objects(author__in=authors)
    result = process_objects(quotes)
    return result


@input_error
def search_by_tag(**kwargs):
    tag = kwargs["value"][0]
    quotes = Quotes.objects(tags=tag)
    result = process_objects(quotes)
    return result


@input_error
def search_by_tags(**kwargs):
    tags = kwargs["value"]
    quotes = Quotes.objects(tags__in=tags)
    result = process_objects(quotes)
    return result


@input_error
def end_of_search(**kwargs):
    return "The end of search. Thank you for using \"quotation_book\"! Bye!"


COMMANDS = {
    "name": search_by_name,
    "names": search_by_names,
    "tag": search_by_tag,
    "tags": search_by_tags,
    "exit": end_of_search,
}


def get_handler(command: str):
    return COMMANDS.get(command.lower())


def main(command_dict:dict) -> bytes:
    command = command_dict.get("command", "")
    handler = get_handler(command)

    if handler:
        return handler(**command_dict).encode(encoding="utf-8")

    bad_message = "Can not recognize a command! Please, try again."
    return bad_message.encode(encoding="utf-8")


if __name__ == "__main__":
    # output info
    print(
        """\nInfo:
        Command format: [command]: [value[1],value[2],...,value[n]]
        Available commands: 'name', 'names', 'tag', 'tags'
        For exit enter 'exit'.\n"""
    )
   
    # output result
    while True:
        user_input = input("\nEnter your command: ")

        command_dict = parcing_data(user_input)
        command = command_dict.get("command", "")

        if command:
            result = main(command_dict).decode()

            if command == "exit":
                print(result)
                break

            output = f"Result:\n{result if result else "nothing find"}"
            print(output)
