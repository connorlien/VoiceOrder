
def process_order(order):
    tags = order["payload"]
    result = {
        "order_name": "",
        "amount_of_drinks": 1,
        "drink_size": "regular",
        "ice": 100,
        "sweetness": 100,
        "toppings": [],
    }
    for tag in tags:
        result[tag["displayName"]] = tag["textExtraction"]["textSegment"]["content"]
    result["amount_of_drinks"] = int(result["amount_of_drinks"])
    return result

test = {
  "payload": [
    {
      "annotationSpecId": "2333535309070860288",
      "displayName": "order_name",
      "textExtraction": {
        "score": 0.99900645,
        "textSegment": {
          "startOffset": "62",
          "endOffset": "85",
          "content": "black milk tea"
        }
      }
    },
    {
      "annotationSpecId": "1180613804464013312",
      "displayName": "sweetness",
      "textExtraction": {
        "score": 0.9992172,
        "textSegment": {
          "startOffset": "90",
          "endOffset": "117",
          "content": "developmental abnormalities"
        }
      }
    },
    {
      "annotationSpecId": "2333535309070860288",
      "displayName": "SpecificDisease",
      "textExtraction": {
        "score": 0.999485,
        "textSegment": {
          "startOffset": "127",
          "endOffset": "159",
          "content": "Familial hypobetalipoproteinemia"
        }
      }
    },
    {
      "annotationSpecId": "1180613804464013312",
      "displayName": "DiseaseClass",
      "textExtraction": {
        "score": 0.9991241,
        "textSegment": {
          "startOffset": "166",
          "endOffset": "195",
          "content": "autosomal codominant disorder"
        }
      }
    },
    {
      "annotationSpecId": "2333535309070860288",
      "displayName": "SpecificDisease",
      "textExtraction": {
        "score": 0.9990812,
        "textSegment": {
          "startOffset": "346",
          "endOffset": "369",
          "content": "hypobetalipoproteinemia"
        }
      }
    },
    {
      "annotationSpecId": "1180613804464013312",
      "displayName": "DiseaseClass",
      "textExtraction": {
        "score": 0.9863149,
        "textSegment": {
          "startOffset": "428",
          "endOffset": "453",
          "content": "coronary vascular disease"
        }
      }
    },
    {
      "annotationSpecId": "2333535309070860288",
      "displayName": "SpecificDisease",
      "textExtraction": {
        "score": 0.9989736,
        "textSegment": {
          "startOffset": "597",
          "endOffset": "620",
          "content": "hypobetalipoproteinemia"
        }
      }
    }
  ]
}

print(process_order(test))