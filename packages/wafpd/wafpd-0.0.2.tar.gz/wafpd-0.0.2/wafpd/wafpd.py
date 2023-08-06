from nltk.tokenize import word_tokenize

commands = ["sort", "filter", "group", "rank", "data", "analyse", "save", "all", "clear",
            "information", "fill", "split", "join", "add", "find", "average", "max", "min", "value",
            "odd", "even", "or", "select", "create", "into", "database", "table", "relate", "in",
            "between", "alter", "int", "varchar", "primary", "update", "from", "where", "on", "delete",
            "commit", "plot", "ranked", "age", "salary", "bonus"]
ignore_commands = ["give", "me", "i", "want", "to", "it", "and"]

def word_analyzer(interface_input):
    picfi = word_tokenize(interface_input)
    common_elements = [element for element in picfi if element in commands]
    print(common_elements)

    starting_index1 = interface_input.find("average value of") + 17
    ending_index1 = interface_input.find("that") - 1
    action_word = interface_input[starting_index1:ending_index1]
    print(action_word)
