#!/bin/bash

# Generate GPT-3 inputs for paraphrasing with thingtalk
# Input: Groundtruth JSON
# {
#     data: [
#       {
#           question: "Question",
#           thingtalk: "ThingTalk",
#           ...
#        }
#     ]
# }
# Output: JSON of questions, parsed ThingTalk, and answers
# {
#     data: [
#       {
#           "question": "Question",
#           "gold": "ThingTalk",
#           "properties": "ThingTalk properties",
#           "gold_answer": "Answer"
#       },
#     ]
# }
python src/utils/gen_gpt_input.py \
    --input "src/data/training_files/dev.json" \
    --output_file "src/data/input/gpt3_dev.json"

python src/utils/gen_gpt_input.py \
    --input "src/data/training_files/dev.json" \
    --output_file "src/data/input/tt_gpt3_dev.json" \
    --use_thingtalk

# Run GPT-3 with specified prompt and question inputs
# Input: JSON of questions, parsed ThingTalk, and answers
# Output: JSON of questions and corresponding paraphrases
# {
#     data: [
#       {
#           question: "Question",
#           paraphrase: "Paraphrase",
#        }
#     ]
# }
python src/generator.py \
    --prompt_template_file "src/data/prompts/paraphrase.prompt" \
    --input_file "src/data/input/gpt3_dev.json" \
    --output_file "src/data/input/gpt3_paraphrases_dev.json" \
    --engine text-davinci-002 \
    --num_gen 1 \
    --temperature 0.8 \
    --frequency_penalty 0.5 \
    --presence_penalty 0.5

python src/generator.py \
    --prompt_template_file "src/data/prompts/paraphrase.prompt" \
    --input_file "src/data/input/tt_gpt3_dev.json" \
    --output_file "src/data/input/davinci2/gpt3_tt_paraphrases_dev.json" \
    --engine text-davinci-002 \
    --num_gen 1 \
    --temperature 0.8 \
    --frequency_penalty 0.5 \
    --presence_penalty 0.5 \
    --use_thingtalk

# Generate answers to GPT-3 paraphrases
# Input: JSON of questions and corresponding paraphrases
# {
#     data: [
#       {
#           question: "Question",
#           paraphrase: "Paraphrase",
#        }
#     ]
# }
# Output: JSON of question and semantic parser output
# {
#     data: [
#       {
#           question: "Question",
#           thingtalk: "ThingTalk",
#           ...
#        }
#     ]
# }
# node index.js

# Output question query and answer accuracy
python src/utils/eval.py \
    --input_file "src/data/output/davinci2/gpt3_paraphrases_dev.json" \
    --baseline_file "src/data/output/baseline/answer_dev.json" \
    --twoshot

python src/utils/eval.py \
    --input_file "src/data/output/davinci2/gpt3_tt_paraphrases_dev.json" \
    --baseline_file "src/data/output/baseline/answer_dev.json" \
    --twoshot