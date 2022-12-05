import argparse
import json
from statistics import mode

def get_arg_parse():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True, help='Where to read input questions from.')
    args = parser.parse_args()

    return args


def get_query_accuracy_2(file):
    with open(file) as json_file:
        data = json.load(json_file)['data']
    
    
    questions_answer = {}
    for question in data:
        q = question['question']
        if q not in questions_answer.keys():
            questions_answer[q] = 0

        if question['gold'] == question['thingtalk']:
            questions_answer[q] += 1
            # print(q)
            # print(question['thingtalk'])

    correct = 0
    total = 0
    for key, value in questions_answer.items():
        if value >= 1:
            correct += 1
        total += 1

    accuracy = correct / total
    print("Correct: ", correct)
    print("Total: ", total)
    print("Query Accuracy: ", accuracy)
    return accuracy


def get_answer_accuracy_2(file):
    with open(file) as json_file:
        data = json.load(json_file)['data']
    
    
    questions_answer = {}
    for question in data:
        q = question['question']
        if q not in questions_answer.keys():
            questions_answer[q] = 0

        if question['answer'] != "" and question['gold_answer'] != "None":
            if question['gold_answer'] == question['answer']:
                questions_answer[q] += 1
                # print(q)
                # print(question['thingtalk'])

    correct = 0
    total = 0
    for key, value in questions_answer.items():
        if value >= 1:
            correct += 1
        total += 1

    accuracy = correct / total
    print("Correct: ", correct)
    print("Total: ", total)
    print("Answer Accuracy: ", accuracy)
    return accuracy
    
    # questions_thingtalk = {}
    # for question in data:
    #     if question not in questions_thingtalk:
    #         questions_thingtalk[question] = []
    #     questions_thingtalk[question].append(question['thingtalk'])

    # correct = 0
    # total = 0
    # questions_answers = {}
    # for key, value in questions_thingtalk.items():
    #     answer = mode(value)
    #     questions_answers[key] = answer
    
    # for question in data:

    #     if question['gold'] == question['thingtalk']:
    #         correct += 1
    #     total += 1

    # accuracy = correct / total
    # print("Correct: ", correct)
    # print("Total: ", total)
    # print("Query Accuracy: ", accuracy)
    # return accuracy


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
    print("Correct: ", correct)
    print("Total: ", total)
    print("Query Accuracy: ", accuracy)
    return accuracy


def get_answer_accuracy(file):
    with open(file) as json_file:
        data = json.load(json_file)['data']

    correct = 0
    total = 0
    for question in data:
        if question['answer'] != "" and question['gold_answer'] != "None":
            if question['gold_answer'] == question['answer']:
                correct += 1
        total += 1

    accuracy = correct / total
    print("Correct: ", correct)
    print("Total: ", total)
    print("Answer Accuracy: ", accuracy)
    return accuracy


if __name__ == "__main__":
    args = get_arg_parse()
    get_query_accuracy_2(args.input_file)
    get_answer_accuracy_2(args.input_file)
    # get_query_accuracy(args.input_file)
    # get_answer_accuracy(args.input_file)
