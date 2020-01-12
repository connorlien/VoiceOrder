import time
import jwt
import requests
import json
import difflib


def find_closest_match(order, order_possibilities):
    if order in order_possibilities:
        return order
    list_of_attempts = []
    for possible_order in order_possibilities:
        possible_order_words = possible_order.split(" ")
        order_words = order.split(" ")
        if set(possible_order_words) == set(order_words):
            return possible_order
    return difflib.get_close_matches(order, order_possibilities, 1, 0)[0]


def get_menu():
    menu_text = open("menu.txt", "r")
    menu_list = [i[:-1] for i in menu_text.readlines()]
    menu_text.close()

    menu_dict = {}

    for line in menu_list:
        menu_line = line.split("/", 4)
        menu_dict[menu_line[0].lower()] = {
            "regular": float(menu_line[1]),
            "large": float(menu_line[2]),
            "hot": float(menu_line[3])
        }

    return menu_dict


def get_toppings():
    toppings_text = open("toppings.txt", "r")
    toppings_list = [i[:-1] for i in toppings_text.readlines()]
    toppings_text.close()

    toppings_dict = {}

    for line in toppings_list:
        toppings_line = line.split("/", 2)
        toppings_dict[toppings_line[0].lower()] = float(toppings_line[1])

    return toppings_dict


def reformat_order(order):  # order is a dictionary in JSON form

    # collect data
    tags = order["payload"]
    menu = get_menu()
    toppings_menu = get_toppings()

    # set default values
    result = {
        "order_name": "",
        "amount_of_drinks": 1,
        "drink_size": "regular",
        "ice": "100",
        "sweetness": "100",
        "topping": [],
        "price": 0.00
    }

    # read from the order
    for tag in tags:
        if tag["displayName"] == "topping":
            result["topping"].append(tag["textExtraction"]["textSegment"]["content"])
        elif tag["displayName"] != "additive_adjective":
            result[tag["displayName"]] = tag["textExtraction"]["textSegment"]["content"]

    # custom processing
    check_synonyms(result)
    if result["ice"] == "hundred":  result["ice"] = "100"
    if result["sweetness"] == "hundred":  result["sweetness"] = "100"
    if result["ice"] == "no":  result["ice"] = "0"
    if result["sweetness"] == "no":  result["sweetness"] = "0"
    if result["ice"] == "less":  result["ice"] = "75"
    if result["sweetness"] == "less":  result["sweetness"] = "75"
    if result["ice"] == "half":  result["ice"] = "50"
    if result["sweetness"] == "half":  result["sweetness"] = "50"
    result["order_name"] = find_closest_match(result["order_name"], menu.keys())
    for i in range(len(result["topping"])):
        result["topping"][i] = find_closest_match(result["topping"][i], toppings_menu.keys())
    result["ice"], result["sweetness"] = str(result["ice"]) + "%", str(result["sweetness"]) + "%"

    # calculate price
    result["price"] = calculate_price(result, menu, toppings_menu)

    # reformat the order name
    result["order_name"] += " tea"

    return result


# calculates the price of the drink
def calculate_price(order, menu, toppings_menu):
    drink_price = menu[order["order_name"]][order["drink_size"]] * order["amount_of_drinks"]
    toppings_price = sum([toppings_menu[i] for i in order["topping"]])
    return round(drink_price + toppings_price, 2)


# checks for synonyms amongst possible order and changes them, like pearls --> boba
def check_synonyms(order):
    order["amount_of_drinks"] = 1 if order["amount_of_drinks"] == "a" else int(order["amount_of_drinks"])

    for i in range(len(order["topping"])):
        if order["topping"][i] == "pearls" or order["topping"][i] == "pearl" or order["topping"][i] == "bubble":
            order["topping"][i] = "boba"
        elif order["topping"][i] == "housemade grass jelly":
            order["topping"][i] = "grass jelly"


# converts a number in words to an int
def text2int(textnum, numwords={}):
    if not numwords:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):   numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    current, result = 0, 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)
        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


def get_authorization_token():
    PRIVATE_KEY_ID_FROM_JSON = "06008be201f2b85860cb38fabbb1f576e63a7336"
    PRIVATE_KEY_FROM_JSON = "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCymWeb8adAA9x0\nceN2nl9c22pIOb97AjrjWUxb5ioSrEp6kdfxI7NL0HfWSivyAFru9uPQVwo+6LXM\nlUhNzTDiY45U8eVxTrPc8+SlQEbNtHv84UbbGZxToVUU4Whl2pi/VegpThRhRr3Z\n25J3zEF20r00nZ3EZ46DdP6ynHxGDUybZfbotq3Ii6j/kb9aQ+mXm9ojWT4hWhSR\nxBclC1Mw/hM1o2qwlBfr1K+5w0HwwK9AZkPGMe1/9zfy/UfjJk4FndoFWjHzyTVE\nKp0YikPnts7nl6BNZP/WsKUUFFgtRXh64lLeoT1X5n7eH1fgKQdCq0/EbfcqjPQE\n5Da+3qANAgMBAAECggEAMgnD2w+p7cgHKILOGWpGypPY47J2QOb/i7n1qFvEluW5\nmjypVTDM56VZJeszA8Lwtznp2vG/958obFC46L9f/lWpR4hcYdIMl4+nlFr9W13B\nTTjqqrEyuMWfOlHq93p2yEiv2n67PAPfZh3cG/9YqgtiIk80qBXhelg5kd5A/Tj9\nwclRweh4UGpYVj3iD3jYN5PZ8Ad/6r7tuO0ujUIb8qR9k1XUD46bK531zbcpGjCm\nMv2LNr24ykN83b874Su3d7lc9wXyOBIX662aRAR/JRFUGOVsCc0KG58usSJxKp3W\nJGlzCBPRyDb/WJTD1G6iOIrjuiwz3e1ESxAChMN76wKBgQDeHnuz6570VxtFl7tb\n+8YW58Mq+vHeW/VyMfrltlUmg6SmWfYAVh/cQa+LOfyWucAJDV2hVYXRN7jT9ipx\nYjzYls7VyLbbJNV0Z0fsmAMzfuuMYQB0T617zLmeIQe0ariamiU0WJfwQFzk2zvv\npuIOe1yudRXUYjIXRskU7+RhowKBgQDN14R7nmakJeJJJOz6MOijfluJ5h+WHUl3\n4yTSVyWjwQzvaJJiCAvWacPco3Rl+RFVJru59rFYaICLabQ0gNkNxC3gcuNxKLGg\nJMVwgW/pKT7ogvx2hB5li4hrTttkPtEzbIIYfHlbUAGtl49Azmyygd+VZTwKsE2A\nqBnXXgDyjwKBgFsdnhkcWsRYxzMxHwaIraXPxNvovTc9+d2yav24Yg2+ithCpwtU\nSRWNTHmMe/VIlWIhPXtlHdPJS+SHYrnIVrVyh75i67/RyE5L39FKOmXxdqbLU+hi\nlwPl427elc6IyNmCyihC/3DqtjCbTmbsymaubEKUfTP2ZB3wR6RzE/iJAoGAR7ys\nd0ilDOAHFObBkBArg48t58lDiNV8HUQUORoWDBPjpiwTmAal2XvSvrpYfpFm8P4m\nvpCzDdSdt/iGzSV6f8m3E1n22iEMhntKNANoNSIiwnWj9snkrg8K5Br/athZoEpY\nrJ/0y1X+v7jqO/O0/iE1AqPdYPxAhm4PU3d3bRECgYAfjsOHcWVBMHm+HjnEnYZD\nSsE5sq68Tt/NqZU++gcUc/UzfH+LBfVWzO+4SxTyDvPfwa+P9UfQJbvMisMsa/ZD\nCMRcyrzAwpwXEZg2lCCwwO1VX+B+G7pLhlVgN6OzV88w+1OgWAkBJ7+N7tJjqBr1\ngONYUuIaD7VIyE3n8Sq3TA==\n-----END PRIVATE KEY-----\n"
    iat = time.time()
    exp = iat + 3600
    payload = {'iss': 'firstserviceaccount@iwillnotscrewupthistime.iam.gserviceaccount.com',
               'sub': 'firstserviceaccount@iwillnotscrewupthistime.iam.gserviceaccount.com',
               "scope": "https://www.googleapis.com/auth/cloud-platform",
               'aud': 'https://oauth2.googleapis.com/token',
               'iat': iat,
               'exp': exp}
    additional_headers = {'kid': PRIVATE_KEY_ID_FROM_JSON}

    signed_jwt = jwt.encode(payload, PRIVATE_KEY_FROM_JSON, headers=additional_headers,
                            algorithm='RS256')

    data = "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=" + str(signed_jwt, 'utf-8')
    url = "https://oauth2.googleapis.com/token"
    headers = {}
    http_response = requests.request("POST", url, headers=headers,
                                     data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                           "assertion": str(signed_jwt, 'utf-8')})
    response = http_response.json()
    # return response
    return response["access_token"]


def request_from_model(content, token):
    # url = "https://automl.googleapis.com/v1/projects/project-id/locations/location-id/models/model-id:predict"
    url = "https://automl.googleapis.com/v1/projects/563618380092/locations/us-central1/models/TEN7419271367767359488:predict"
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json; charset=utf-8"}
    data = {
        "payload": {
            "textSnippet": {
                "content": content,
                "mime_type": "text/plain"
            }
        }
    }
    http_response = requests.request("POST", url, headers=headers, json=data)
    response = http_response.json()
    return response


def add_object_to_db(dict):
    url = "https://sbhacks-c08dc.firebaseio.com/orders.json"
    headers = {}
    http_response = requests.request("GET", url, headers=headers)
    response = http_response.json()
    response["order_list"].append(dict)
    http_response = requests.request("PUT", url, headers=headers, data=json.dumps(response))
    response = http_response.json()


def process_user_order(content, token):
    # request_from_model("Targeted modification of the apolipoprotein B gene results in hypobetalipoproteinemia and developmental abnormalities in mice.	Familial hypobetalipoproteinemia is an autosomal codominant disorder resulting in a dramatic reduction in plasma concentrations of apolipoprotein ( apo ) B , cholesterol , and beta-migrating lipoproteins . A benefit of hypobetalipoproteinemia is that mildly affected individuals may be protected from coronary vascular disease . We have used gene targeting to generate mice with a modified Apob allele . Mice containing this allele display all of the hallmarks of human hypobetalipoproteinemia  they produce a truncated apoB protein , apoB70 , and have markedly decreased plasma concentrations of apoB , beta-lipoproteins , and total cholesterol .", get_authorization_token())
    try:
        response_dict = request_from_model(content, token)

        db_object = reformat_order(response_dict)
        add_object_to_db(db_object)

    except Exception as e:
        return False, -1
    return True, db_object["price"]


def init_table():
    url = "https://sbhacks-c08dc.firebaseio.com/orders.json"
    headers = {}
    http_response = requests.request("PUT", url, headers=headers, data=json.dumps({"order_list": [
        {"keys": ["order_name", "drink_size", "amount_of_drinks", "ice", "sweetness", "topping", "price"]}]}))
    response = http_response.json()
    print(response)
