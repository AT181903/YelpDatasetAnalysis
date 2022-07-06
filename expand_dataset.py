import ast


def expand(row, dict):
    for key, values in dict.items():
        row[key] = values
    return row


def expand_hours_feature(row):
    try:
        return expand(row, ast.literal_eval(row['hours']))
    except:
        return row

def expand_attributes_feature(row):
    # print(row['attributes'])
    try:
        return expand(row, ast.literal_eval(row['attributes']))
    except:
        return row


def expand_business_parking_feature(row):
    try:
        return expand(row, ast.literal_eval(row['BusinessParking']))
    except:
        return row