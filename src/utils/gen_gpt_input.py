import argparse
import json
import re

def get_arg_parse():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True, help='Where to read input questions from.')
    parser.add_argument('--output_file', type=str, default="src/data/input/paraphrase.json", help='Where to write the outputs.')
    parser.add_argument('--use_thingtalk', action='store_true', help='Generate GPT-3 using thingtalk')

    args = parser.parse_args()

    return args


def parse_thingtalk(thingtalk, start="[ ", end=" ]"):
    words = "sort ("
    if words in thingtalk:
        start_idx = thingtalk.find(words) + len(words) - 1
        thingtalk = thingtalk[start_idx:]
        properties = thingtalk.strip().split()[1]

    words = "contains ("
    if words in thingtalk:
        start_idx = thingtalk.find(words) + len(words) - 1
        end_idx = thingtalk.find(',') + 1
        properties = thingtalk[start_idx:end_idx].strip().split("/")
        properties = [" ".join(prop.split("_")) for prop in properties]
    
        thingtalk = ""
        for prop in properties[:-1]:
            thingtalk += prop + ", "
        thingtalk += properties[-1]

    words = "contains~ ("
    if words in thingtalk:
        start_idx = thingtalk.find(words) + len(words) - 1
        end_idx = thingtalk.find(',') + 1
        properties = thingtalk[start_idx:end_idx].strip().split("/")
        properties = [" ".join(prop.split("_")) for prop in properties]
    
        thingtalk = ""
        for prop in properties[:-1]:
            thingtalk += prop + ", "
        thingtalk += properties[-1]
    
    words = "count ("
    if words in thingtalk:
        start_idx = thingtalk.find(words) + len(words) - 1
        thingtalk = thingtalk[start_idx:]
        properties = thingtalk.strip().split()[1]
    
    start_idx = thingtalk.find(start) + len(start)
    end_idx = thingtalk.find(end)
    properties = thingtalk[start_idx:end_idx].strip().split("/")
    properties = [" ".join(prop.split("_")) for prop in properties]

    prop_words = ""
    for prop in properties[:-1]:
        prop_words += prop + ", "
    prop_words += properties[-1]
    prop_words = prop_words.strip("< ").strip(" >")

    return prop_words


def save_json(dictionary, file):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    
    # Writing to sample.json
    with open(file, "w") as outfile:
        outfile.write(json_object)


def generate_paraphrase(questions_file, output_file):
    with open(questions_file) as json_file:
        questions = json.load(json_file)['data']
        paraphrase_prompts = {}
        paraphrase_prompts["data"] = []

        for data in questions:
            prompt = {}
            prompt["question"] = data['question']
            prompt["gold"] = data['gold']
            prompt["gold_answer"] = data["gold_answer"]
            paraphrase_prompts["data"].append(prompt)

    save_json(paraphrase_prompts, output_file)


def generate_thingtalk_paraphrase(questions_file, output_file):
    with open(questions_file) as json_file:
        questions = json.load(json_file)['data']
        paraphrase_prompts = {}
        paraphrase_prompts["data"] = []

        for data in questions:
            question = data['question']
            gold = data['gold']
            thingtalk = data['thingtalk']
            prop_words = parse_thingtalk(thingtalk)

            prompt = {}
            prompt["question"] = question
            prompt["gold"] = gold
            prompt["properties"] = prop_words
            prompt["gold_answer"] = data["gold_answer"]
            paraphrase_prompts["data"].append(prompt)

    save_json(paraphrase_prompts, output_file)

if __name__ == "__main__":
    args = get_arg_parse()
    if args.use_thingtalk:
        generate_thingtalk_paraphrase(args.input_file, args.output_file)
    else:
        generate_paraphrase(args.input_file, args.output_file)

# python src/scripts/gen_thingtalk_paraphrase --input "/Users/juliaxu/Documents/F2022/CS224V/project/gpt3-example/src/data/output/thingtalk_answer.json" --output_file "output.txt"