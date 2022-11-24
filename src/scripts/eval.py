import argparse
import json

def get_arg_parse():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True, help='Where to read input questions from.')
    args = parser.parse_args()

    return args


def get_query_accuracy(file):
    with open(file) as json_file:
        data = json.load(json_file)['data']

    correct = 0
    total = 0
    for question in data:
        if question['gold'] == question['thingtalk']:
            correct += 1
        total += 1

    accuracy = correct / total
    print("Accuracy: ", accuracy)
    return accuracy


if __name__ == "__main__":
    args = get_arg_parse()
    get_query_accuracy(args.input_file)
