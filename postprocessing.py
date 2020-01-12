from boberMenuTime import *

def process_order(order): # order is a dictionary in JSON form

    # collect data
    tags = order["payload"]

    # set default values
    result = {
        "order_name": "",
        "amount_of_drinks": 1,
        "drink_size": "regular",
        "ice": 100,
        "sweetness": 100,
        "topping": [],
        "price": 0.00
    }

    # read from the order
    for tag in tags:
        if tag["displayName"] == "topping":
            result["topping"].append(tag["textExtraction"]["textSegment"]["content"])
        else:
            result[tag["displayName"]] = tag["textExtraction"]["textSegment"]["content"]

    #custom processing
    if result["amount_of_drinks"] == "a":
        result["amount_of_drinks"] = 1
    else:
        result["amount_of_drinks"] = int(result["amount_of_drinks"])
    result["price"] = calculate_price(result)

    return result


def calculate_price(order):

    # load data
    menu = get_menu()
    toppings_menu = get_toppings()

    # calculate drink and toppings prices
    drink_price = menu[order["amount_of_drinks"]][order["drink_size"]] * order["amount_of_drinks"]
    toppings_price = sum([toppings_menu[i] for i in order["topping"]])

    return drink_price + toppings_price


test = {
  "payload": [
    {
      "annotationSpecId": "705695150008958976",
      "displayName": "additive_adjective",
      "textExtraction": {
        "score": 0.99953187,
        "textSegment": {
          "startOffset": "6",
          "endOffset": "11",
          "content": "order"
        }
      }
    },
    {
      "annotationSpecId": "1491432547496755200",
      "displayName": "amount_of_drinks",
      "textExtraction": {
        "score": 0.99947494,
        "textSegment": {
          "startOffset": "12",
          "endOffset": "13",
          "content": "a"
        }
      }
    },
    {
      "annotationSpecId": "5878079322043973632",
      "displayName": "drink_size",
      "textExtraction": {
        "score": 0.99950624,
        "textSegment": {
          "startOffset": "14",
          "endOffset": "19",
          "content": "large"
        }
      }
    },
    {
      "annotationSpecId": "702317450288431104",
      "displayName": "order_name",
      "textExtraction": {
        "score": 0.999563,
        "textSegment": {
          "startOffset": "20",
          "endOffset": "30",
          "content": "black milk"
        }
      }
    },
    {
      "annotationSpecId": "1398827280158949376",
      "displayName": "sweetness",
      "textExtraction": {
        "score": 0.9994066,
        "textSegment": {
          "startOffset": "40",
          "endOffset": "45",
          "content": "fifty"
        }
      }
    }
  ]
}

print(process_order(test))