# written by Connor Lien for SBHacks

from api_handler import *


def get_menu():
    menu_text = open("menu.txt", "r")
    menu_list = [i[:-1] for i in menu_text.readlines()]
    menu_text.close()

    menu_dict = {}

    for line in menu_list:
        menu_line = line.split("/",4)
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
        toppings_line = line.split("/",2)
        toppings_dict[toppings_line[0].lower()] = float(toppings_line[1])

    return toppings_dict

def reformat_order(order): # order is a dictionary in JSON form

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
    result["order_name"] = find_closest_match(result["order_name"], menu.keys())
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
        if order["topping"][i] == "pearls" or order["topping"][i] == "pearl":
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

# a test JSON dictionary to run
test = {
  "payload": [
    {
      "annotationSpecId": "705695150008958976",
      "displayName": "additive_adjective",
      "textExtraction": {
        "score": 0.9995351,
        "textSegment": {
          "startOffset": "6",
          "endOffset": "10",
          "content": "have"
        }
      }
    },
    {
      "annotationSpecId": "1491432547496755200",
      "displayName": "amount_of_drinks",
      "textExtraction": {
        "score": 0.9995581,
        "textSegment": {
          "startOffset": "11",
          "endOffset": "12",
          "content": "a"
        }
      }
    },
    {
      "annotationSpecId": "5878079322043973632",
      "displayName": "drink_size",
      "textExtraction": {
        "score": 0.99946374,
        "textSegment": {
          "startOffset": "13",
          "endOffset": "18",
          "content": "large"
        }
      }
    },
    {
      "annotationSpecId": "702317450288431104",
      "displayName": "order_name",
      "textExtraction": {
        "score": 0.9994789,
        "textSegment": {
          "startOffset": "19",
          "endOffset": "29",
          "content": "black milk"
        }
      }
    },
    {
      "annotationSpecId": "1398827280158949376",
      "displayName": "sweetness",
      "textExtraction": {
        "score": 0.9994167,
        "textSegment": {
          "startOffset": "39",
          "endOffset": "44",
          "content": "25"
        }
      }
    },
    {
      "annotationSpecId": "4193733061407408128",
      "displayName": "ice",
      "textExtraction": {
        "score": 0.9983238,
        "textSegment": {
          "startOffset": "63",
          "endOffset": "74",
          "content": "50"
        }
      }
    },
    {
      "annotationSpecId": "4582907401081978880",
      "displayName": "topping",
      "textExtraction": {
        "score": 0.99956995,
        "textSegment": {
          "startOffset": "92",
          "endOffset": "96",
          "content": "boba"
        }
      }
    },
    {
      "annotationSpecId": "4582907401081978880",
      "displayName": "topping",
      "textExtraction": {
        "score": 0.9995287,
        "textSegment": {
          "startOffset": "101",
          "endOffset": "113",
          "content": "lychee jelly"
        }
      }
    }
  ]
}

print(reformat_order(test))
