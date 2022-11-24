import argparse
import json

def get_arg_parse():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--groundtruth_file', type=str, required=True, help='Where to read input questions from.')
    parser.add_argument('--paraphrase_file', type=str, default="src/data/output/thingtalk_answer.json", help='Where to write the outputs.')

    args = parser.parse_args()

    return args


def get_query_accuracy(groundtruth_file, pred_file):
    with open(groundtruth_file) as json_file:
        groundtruth = json.load(json_file)['data']

    with open(pred_file) as json_file:
        prediction = json.load(json_file)['data']

    correct = 0
    total = 0
    for pred in prediction:
        for gt in groundtruth:
            if pred['question'] == gt['question'] and pred['thingtalk'] == gt['thingtalk']:
                correct += 1
        total += 1

    accuracy = correct / total
    return accuracy


if __name__ == "__main__":
    args = get_arg_parse()
    get_query_accuracy(args.input_file, args.output_file)

# python src/scripts/gen_thingtalk_paraphrase --input "/Users/juliaxu/Documents/F2022/CS224V/project/gpt3-example/src/data/output/thingtalk_answer.json" --output_file "output.txt"