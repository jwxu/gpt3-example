import csv
import json

filepath = "../data/training_files/fewshot.tsv"

def convert_to_json(filepath):
    returnObj = {
        "data": []
    }
    with open(filepath) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file:
            returnObj["data"].append({"Question": line[1], "Gold": line[2]})

        # Serializing json
        json_object = json.dumps(returnObj, indent=4)

        # Writing to sample.json
        with open("../data/training_files/fewshot.json", "w") as outfile:
            outfile.write(json_object)

convert_to_json(filepath)