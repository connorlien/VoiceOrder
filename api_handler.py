
import time
import jwt
import requests
import json
import urllib
import difflib

def get_authorization_token():
    PRIVATE_KEY_ID_FROM_JSON= "06008be201f2b85860cb38fabbb1f576e63a7336"
    PRIVATE_KEY_FROM_JSON = "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCymWeb8adAA9x0\nceN2nl9c22pIOb97AjrjWUxb5ioSrEp6kdfxI7NL0HfWSivyAFru9uPQVwo+6LXM\nlUhNzTDiY45U8eVxTrPc8+SlQEbNtHv84UbbGZxToVUU4Whl2pi/VegpThRhRr3Z\n25J3zEF20r00nZ3EZ46DdP6ynHxGDUybZfbotq3Ii6j/kb9aQ+mXm9ojWT4hWhSR\nxBclC1Mw/hM1o2qwlBfr1K+5w0HwwK9AZkPGMe1/9zfy/UfjJk4FndoFWjHzyTVE\nKp0YikPnts7nl6BNZP/WsKUUFFgtRXh64lLeoT1X5n7eH1fgKQdCq0/EbfcqjPQE\n5Da+3qANAgMBAAECggEAMgnD2w+p7cgHKILOGWpGypPY47J2QOb/i7n1qFvEluW5\nmjypVTDM56VZJeszA8Lwtznp2vG/958obFC46L9f/lWpR4hcYdIMl4+nlFr9W13B\nTTjqqrEyuMWfOlHq93p2yEiv2n67PAPfZh3cG/9YqgtiIk80qBXhelg5kd5A/Tj9\nwclRweh4UGpYVj3iD3jYN5PZ8Ad/6r7tuO0ujUIb8qR9k1XUD46bK531zbcpGjCm\nMv2LNr24ykN83b874Su3d7lc9wXyOBIX662aRAR/JRFUGOVsCc0KG58usSJxKp3W\nJGlzCBPRyDb/WJTD1G6iOIrjuiwz3e1ESxAChMN76wKBgQDeHnuz6570VxtFl7tb\n+8YW58Mq+vHeW/VyMfrltlUmg6SmWfYAVh/cQa+LOfyWucAJDV2hVYXRN7jT9ipx\nYjzYls7VyLbbJNV0Z0fsmAMzfuuMYQB0T617zLmeIQe0ariamiU0WJfwQFzk2zvv\npuIOe1yudRXUYjIXRskU7+RhowKBgQDN14R7nmakJeJJJOz6MOijfluJ5h+WHUl3\n4yTSVyWjwQzvaJJiCAvWacPco3Rl+RFVJru59rFYaICLabQ0gNkNxC3gcuNxKLGg\nJMVwgW/pKT7ogvx2hB5li4hrTttkPtEzbIIYfHlbUAGtl49Azmyygd+VZTwKsE2A\nqBnXXgDyjwKBgFsdnhkcWsRYxzMxHwaIraXPxNvovTc9+d2yav24Yg2+ithCpwtU\nSRWNTHmMe/VIlWIhPXtlHdPJS+SHYrnIVrVyh75i67/RyE5L39FKOmXxdqbLU+hi\nlwPl427elc6IyNmCyihC/3DqtjCbTmbsymaubEKUfTP2ZB3wR6RzE/iJAoGAR7ys\nd0ilDOAHFObBkBArg48t58lDiNV8HUQUORoWDBPjpiwTmAal2XvSvrpYfpFm8P4m\nvpCzDdSdt/iGzSV6f8m3E1n22iEMhntKNANoNSIiwnWj9snkrg8K5Br/athZoEpY\nrJ/0y1X+v7jqO/O0/iE1AqPdYPxAhm4PU3d3bRECgYAfjsOHcWVBMHm+HjnEnYZD\nSsE5sq68Tt/NqZU++gcUc/UzfH+LBfVWzO+4SxTyDvPfwa+P9UfQJbvMisMsa/ZD\nCMRcyrzAwpwXEZg2lCCwwO1VX+B+G7pLhlVgN6OzV88w+1OgWAkBJ7+N7tJjqBr1\ngONYUuIaD7VIyE3n8Sq3TA==\n-----END PRIVATE KEY-----\n"
    iat = time.time()
    exp = iat + 3600
    payload = {'iss': 'firstserviceaccount@iwillnotscrewupthistime.iam.gserviceaccount.com',
               'sub': 'firstserviceaccount@iwillnotscrewupthistime.iam.gserviceaccount.com',
                "scope":"https://www.googleapis.com/auth/cloud-platform",
               'aud': 'https://oauth2.googleapis.com/token',
               'iat': iat,
               'exp': exp}
    additional_headers = {'kid': PRIVATE_KEY_ID_FROM_JSON}
    signed_jwt = jwt.encode(payload, PRIVATE_KEY_FROM_JSON, headers=additional_headers,
                           algorithm='RS256')

    data = "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=" + urllib.parse.quote(str(signed_jwt, 'utf-8'))
    url = "https://oauth2.googleapis.com/token"
    headers = {}
    http_response = requests.request("POST", url, headers=headers, data={"grant_type" : "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion" : str(signed_jwt, 'utf-8')})
    response = http_response.json()
    return response["access_token"]


def request_from_model(content, token):
    #url = "https://automl.googleapis.com/v1/projects/project-id/locations/location-id/models/model-id:predict"
    url = "https://automl.googleapis.com/v1/projects/563618380092/locations/us-central1/models/TEN7419271367767359488:predict"
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json; charset=utf-8"}
    data = {
          "payload" : {
            "textSnippet": {
              "content": content,
              "mime_type": "text/plain"
              }
           }
        }
    http_response = requests.request("POST", url, headers=headers, json=data)
    response = http_response.json()
    print(json.dumps(response, indent=2))
    return response

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



def add_object_to_db(dict):
    url = "https://sbhacks-c08dc.firebaseio.com/orders.json"
    headers = {}
    http_response = requests.request("GET", url, headers=headers)
    response= http_response.json()
    response["order_list"].append(dict)
    http_response = requests.request("PUT", url, headers=headers, data=json.dumps(response))
    response= http_response.json()
    print(response)

def process_user_order(content, token):
    #request_from_model("Targeted modification of the apolipoprotein B gene results in hypobetalipoproteinemia and developmental abnormalities in mice.	Familial hypobetalipoproteinemia is an autosomal codominant disorder resulting in a dramatic reduction in plasma concentrations of apolipoprotein ( apo ) B , cholesterol , and beta-migrating lipoproteins . A benefit of hypobetalipoproteinemia is that mildly affected individuals may be protected from coronary vascular disease . We have used gene targeting to generate mice with a modified Apob allele . Mice containing this allele display all of the hallmarks of human hypobetalipoproteinemia  they produce a truncated apoB protein , apoB70 , and have markedly decreased plasma concentrations of apoB , beta-lipoproteins , and total cholesterol .", get_authorization_token())
    response_dict = request_from_model(content, token)
    db_object = reformat_order(response_dict)
    add_object_to_db(db_object)








#print(request_from_model("Can i have a large milk black tea with fifty percent sugar and one hundred percent ice with boba and lychee jelly", get_authorization_token()))

'''
def get_authorization_token():
    PRIVATE_KEY_ID_FROM_JSON= "aff14801b02cdd134a669f5347bfa196bdb256da"
    PRIVATE_KEY_FROM_JSON = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC8ZlIENPOvOv0s\nUNoHfEiyj1+Sqb3PAK47PkvPsno9zAh9qqFDhbEoapzrAN6PjG89jAm+GDgHZ7DA\nO4zL29ZnUu5XGhOrZ4dKG7zWo+xPuvFMI4RVkpPWh8kcioohRfdq2W6MRVYKjP9g\nOihV02TjHD6vynpVqynOO7e9pCkU3pgxvKFWCuy7BCQ+lJ+c8aSI3QC2tM+6DOTb\n72Tnu8LondXNUBos9fu5rvmf11o6pYO7WaEzkrCTvCShw88wzakP2Ox5Q44jWvaK\nFk6Hqlq9pyXGavO33YkZxIX594ooOLQ3eCJd37Ie6i5vzo6iGeX+2AdyMN0y/qdN\nSYx+aSFtAgMBAAECggEAExUSDZcHb6I77ncp/kQaYOugtIw4y3S4MQv4RctAEm5O\nFdxohRxPe1aBGlR2Nnf09Hjwq65sTmO0RWRCuItFxiViOrRLdbsAuwLgN6VW1CSN\nODcIulokW0BZoGhv4Tri+pGXXuHO+zaYzzhUyYyl1VMRDmElzvONQnROAglUl+Ze\n9+YFXCFR+qlgeB2PXYjT3u4lkWseiDqOVWAYAdbp4SUn3DBxi3HorHr24+9g2hmy\ntuOiAOa66w3tVTNhqlOOjEA3LbLfMOJUvNEcjcnpl5BhOjtxxXqndFeFV+GcVW6K\n4QajQ0FxO/dkFcTX2eqXmIsncwGxL8ca6NaRSfA9gQKBgQD9H+ry7wq/yuSuTbt3\nkMHrwjfk902PUEzv36RG7T4VGq31AEpQ2waJSE6Z8Z9oOgqW9Ox1e9EqQ1yI5y4b\nZqE47FAsvVavevqgV5gmziOle/Tm1smZQqqsSfUfQ+A48y3nUtLiGgvo49d+uDYT\neLGYDDyAGRE2655VWZkD2rmj/QKBgQC+ii72SIHoIyG7JcJsMJXKN5CmNz1LPJX5\nxTR21jQbLMTghIHTCv7Kqp9CpPPOxfbB3gPtwq4r7IhRo5Jt63KEWs7iNxpEGGPS\nfT08DYEtrenAB+aeERC7/g0yIWvsH9/Td0qcNcMbUle3nfO+FS6NOp6dP1FQmyFG\n7J0Xd70WMQKBgF0Q/zGS8kDSOIJd0i+D6cjk/+gPhVTMEX2gnKX3VHwt8wfBs5FG\n9oBDNaMkU5fev0YBh28qtxzy53LujOVGNsDXIiNQ+i5K6RtLGYYrBLAzgzfcgQL4\noAf4qUd1jVtjDd2fdinrqbVXEERnNnqyRZnB5fyzOsEWoICBEOF56geBAoGBAIzM\n9ikeqYiONYXjQEnMmVQGPYjmdw/a5ITe+ob6gSS3r4CtynXWwTOoY+nOlS/uUAsw\n8bxHyYdB0fZqJnG9tDEkHY9C4tEBKPrJe2+eFyBXTM2PyRZzS+dvs/aghezGHRNa\nKrNGczgEYDearByB8JWChOV0fbVP/YY4oVlPLVZxAoGAEeqViUuMdqGHYHxJXY94\nrQR7V+yw3h0Wl06HqT9vQy5BO+zhrLifoSc1dmUXsvrsuSy2SnEdPQyqZbVq8BFF\nD6m3UOs+yV20w5UljCpG8kzGNrMbOFWBpz8exZ8hVww0VZULlrbfYdpR65xby+vA\nRPP2E3TBRgKNNmWLowBdfKA=\n-----END PRIVATE KEY-----\n"
    iat = time.time()
    exp = iat + 3600
    service_account = "serviceaccounttrial3@my-first-nlp-264509.iam.gserviceaccount.com"
    payload = {'iss': service_account,
               'sub': service_account,
                "scope":"https://www.googleapis.com/auth/cloud-platform",
               'aud': 'https://oauth2.googleapis.com/token',
               'iat': iat,
               'exp': exp}
    additional_headers = {'kid': PRIVATE_KEY_ID_FROM_JSON}
    signed_jwt = jwt.encode(payload, PRIVATE_KEY_FROM_JSON, headers=additional_headers,
                           algorithm='RS256')

    data = "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=" + urllib.parse.quote(str(signed_jwt, 'utf-8'))
    url = "https://oauth2.googleapis.com/token"
    headers = {}
    http_response = requests.request("POST", url, headers=headers, data={"grant_type" : "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion" : str(signed_jwt, 'utf-8')})
    response = http_response.json()
    return response["access_token"]
    #return response

print(get_authorization_token())
'''
