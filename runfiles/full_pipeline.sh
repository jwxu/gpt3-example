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
python src/scripts/gen_thingtalk_paraphrase.py \
    --input "src/data/output/thingtalk_answer.json" \
    --output_file "src/data/input/thingtalk_paraphrases.txt"

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
    --prompt_template_file "src/data/prompts/thingtalk_paraphrase.prompt" \
    --input_file "src/data/input/thingtalk_paraphrases.txt" \
    --output_file "src/data/output/gpt3_thingtalk_paraphrases.json" \
    --engine text-curie-001 \
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
python src/scripts/eval.py \
    --groundtruth_file "data/training_files/fewshot.json" \
    --prediction_file "data/output/thingtalk_answer.json" 