import json

reader = open("training_data_5.txt", "r")
data = [i[:-1] for i in reader.readlines()]

for i in range(len(data)):
    writer = open("file" + str(i+500) + ".jsonl", "w+", encoding='utf-8')
    writer.write(json.dumps({"text_snippet":{"content": data[i].strip()}}, ensure_ascii=False))