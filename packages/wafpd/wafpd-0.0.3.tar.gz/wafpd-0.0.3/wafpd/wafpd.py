from nltk.tokenize import word_tokenize
import pandas as pd

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

def data_analyze(datatype):
    dt_type = datatype.split(".")
    if "csv" in dt_type:
        csv_data = "csv"
        return pd.read_csv(csv_data)

    elif "exel" in dt_type:
        exel_data = "exel"
        return pd.read_excel(exel_data)

    elif "json" in dt_type:
        json_data = "json"
        return pd.read_json(json_data)
    
    elif "txt" in dt_type :
        txt_data = "txt"
        return pd.read_txt(txt_data)


