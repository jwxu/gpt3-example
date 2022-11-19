import argparse
import json

def get_arg_parse():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True, help='Where to read input questions from.')
    parser.add_argument('--output_file', type=str, default="src/data/input/thingtalk_paraphrase.txt", help='Where to write the outputs.')

    args = parser.parse_args()

    return args


def parse_thingtalk(thingtalk, start="[ ", end=" ]"):
    start_idx = thingtalk.find(start) + len(start)
    end_idx = thingtalk.find(end)
    properties = thingtalk[start_idx:end_idx].strip().split("/")
    properties = [" ".join(prop.split("_")) for prop in properties]

    return properties


def generate_thingtalk_paraphrase(questions_file, output_file):
    with open(questions_file) as json_file:
        questions = json.load(json_file)['data']
        paraphrase_prompts = ""

        for data in questions:
            question = data['question']
            thingtalk = data['thingtalk']
            sparql = data['sparql']
            answer = data['answer']
            props = parse_thingtalk(thingtalk)
            prop_words = ""
            for prop in props[:-1]:
                prop_words += prop + ", "
            prop_words += props[-1]

            paraphrase_prompts += f"Paraphrase \"" + question + "\" using the words \"" + prop_words + "\"\n"

    with open(output_file, "w") as file:
        file.write(paraphrase_prompts)

if __name__ == "__main__":
    args = get_arg_parse()
    generate_thingtalk_paraphrase(args.input_file, args.output_file)

# python src/scripts/gen_thingtalk_paraphrase --input "/Users/juliaxu/Documents/F2022/CS224V/project/gpt3-example/src/data/output/thingtalk_answer.json" --output_file "output.txt"