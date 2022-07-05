import json

def string_to_dict(string):
    return json.loads(string.replace("'", '"'))

def expand(row, dict):
    for key, values in dict.items():
        row[key] = values
    return row


def expand_hours_feature(row):
    return expand(row, string_to_dict(row['hours']))

def expand_attributes_feature(row):
    return expand(row, string_to_dict(row['attributes']))
