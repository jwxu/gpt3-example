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
# Output: Text file of list of questions
python src/utils/gen_gpt_input.py \
    --input "src/data/training_files/fewshot.json" \
    --output_file "src/data/input/thingtalk_paraphrases.json" \
    --use_thingtalk

python src/utils/gen_gpt_input.py \
    --input "src/data/training_files/fewshot.json" \
    --output_file "src/data/input/paraphrases.json"

# Run GPT-3 with thingtalk paraphrase inputs
# Input: Text file of list of questions
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
    --input_file "src/data/input/paraphrases.json" \
    --output_file "src/data/input/gpt3_paraphrases.json" \
    --engine text-curie-001 \
    --num_gen 3

# Run GPT-3 with simplified paraphrase inputs
# Input: JSON file of list of questions
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
    --prompt_template_file "src/data/prompts/simplify.prompt" \
    --input_file "src/data/input/paraphrases.json" \
    --output_file "src/data/input/gpt3_paraphrases_simplified.json" \
    --engine text-davinci-003 \
    --num_gen 3

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

# Output question query accuracy
python src/utils/eval.py \
    --input_file "src/data/output/paraphrase_answer.json"
