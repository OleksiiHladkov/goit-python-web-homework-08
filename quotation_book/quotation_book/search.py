from models import Author, Quotes


def parcing_data(data: str):
    result = {}

    data_list = data.split(":")

    if len(data_list):
        result["command"] = data_list[0]
        if len(data_list) > 1:
            result["value"] = data_list[1].strip().split(",")

    return result


def input_error(handler_func):
    def inner_func(**kwargs):
        try:
            result = handler_func(**kwargs)
        except KeyError as key:
            result = f"Search is not possible: {key} is not found"

        return result

    return inner_func


@input_error
def search_by_name(**kwargs):
    return kwargs["value"]


@input_error
def search_by_tag(**kwargs):
    pass


@input_error
def search_by_tags(**kwargs):
    pass


@input_error
def end_of_search(**kwargs):
    return "The end of search. Thank you for using! Bye!"


COMMANDS = {
    "name": search_by_name,
    "tag": search_by_tag,
    "tags": search_by_tags,
    "exit": end_of_search,
}


def get_handler(command: str):
    return COMMANDS.get(command.lower())


def main():
    while True:
        user_input = input("Enter your command: ")

        command_dict = parcing_data(user_input)

        command = command_dict.get("command", "")

        if command:
            handler = get_handler(command)

            if handler:
                result = handler(**command_dict)

                if command == "exit":
                    print(result, "\n")
                    break

                print(result, "\n")
                continue

        # if "while" not break or not continue - is bad command
        print("Can not recognize a command! Please, try again.", "\n")


if __name__ == "__main__":
    print(
        "\nInfo:\nCommand format: [command]: [value[1],value[2],...,value[n]]\nAvailable commands: 'name', 'tag', 'tags'\nFor exit enter 'exit'.\n"
    )
    main()
