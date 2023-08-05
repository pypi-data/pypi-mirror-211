fav_movies = [
    "The Holy Grail",
    1975,
    "Terry Jones & Terry Gilliam",
    91,
    [
        "Graham Chapman",
        ["Michael Palin", "John Cleese", "Terry Giliam", "Eric Idle", "Terry Jones"],
    ],
]

"""This is the 'nester.py' module, and it provides one function called print_lol() which prints lists that 
    may or may not include nexted lists."""


def print_lol(list):
    """This function takes a positional argument called 'list', which is any Python list (of, possibly, nested lists).
    Each data item in the provided list is (recursively) print to the screen on its own line.
    """

    for item in list:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)


print_lol(fav_movies)
