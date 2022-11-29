import argparse
import json

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
    start_idx = thingtalk.find(start) + len(start)
    end_idx = thingtalk.find(end)
    properties = thingtalk[start_idx:end_idx].strip().split("/")
    properties = [" ".join(prop.split("_")) for prop in properties]

    return properties


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
            props = parse_thingtalk(gold)
            prop_words = ""
            for prop in props[:-1]:
                prop_words += prop + ", "
            prop_words += props[-1]

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