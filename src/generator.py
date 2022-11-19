import argparse
from tqdm import tqdm
import json

from utils.neural_worker import NeuralWorker

def get_arg_parse():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt_template_file', type=str, required=True, help='The path to the file containing the GPT-3 prompt.')
    parser.add_argument('--input_file', type=str, required=True, help='Where to read input questions from.')
    parser.add_argument('--output_file', type=str, required=True, help='Where to write the outputs.')
    parser.add_argument('--engine', type=str, required=True,
                        choices=['ada',
                                 'text-ada-001',
                                 'babbage',
                                 'text-babbage-001',
                                 'curie',
                                 'text-curie-001',
                                 'davinci',
                                 'text-davinci-001',
                                 'text-davinci-002'],
                        help='The GPT-3 engine to use.')  # choices are from the smallest to the largest model

    parser.add_argument('--num_gen', type=int, default=1, required=False, help='Number of turns to continue each dialog for (default: 1')

    # GPT-3 generation hyperparameters
    parser.add_argument('--max_tokens', type=int, default=40, required=False, help='')
    parser.add_argument('--temperature', type=float, default=0.8, required=False, help='')
    parser.add_argument('--top_p', type=float, default=0.9, required=False, help='')
    parser.add_argument('--frequency_penalty', type=float, default=0.0, required=False, help='')
    parser.add_argument('--presence_penalty', type=float, default=0.0, required=False, help='')
    parser.add_argument('--stop_tokens', nargs='+', type=str, default=None, required=False, help='Stop tokens for generation')

    args = parser.parse_args()

    return args


def gen_question(args):
    """
    Use GPT-3 to generate alternative questions
    """
    # Read file of input questions
    file = open(args.input_file)
    all_questions = file.readlines()

    neural_worker = NeuralWorker(prompt_template_file=args.prompt_template_file, engine=args.engine)

    question_gen = {}
    question_gen['data'] = []
    prev_reply = ""
    for question in tqdm(all_questions):
        for _ in range(args.num_gen):
            question_para = {}
            question_para["question"] = question

            filled_prompt = neural_worker.fill_prompt_template(history=question)
            reply = neural_worker.generate(input_text=filled_prompt, args=args, postprocess=True, max_tries=1)
            if len(reply) == 0:
                # handle the case where the output of GPT-3 only contains whitespace, so the above function returns and empty string
                print('Empty generated output. Stopping the dialog early.')
                break

            if reply != prev_reply:
                question_para['paraphrase'] = reply
                question_gen['data'].append(question_para)
                prev_reply = reply

    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(question_gen, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    args = get_arg_parse()
    gen_question(args)
