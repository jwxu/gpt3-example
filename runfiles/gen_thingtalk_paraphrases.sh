#!/bin/bash

python src/scripts/gen_thingtalk_paraphrase.py \
    --input "src/data/training_files/fewshot.json" \
    --output_file "src/data/input/thingtalk_paraphrases.txt"