python src/generator.py \
    --prompt_template_file src/data/prompts/simplify.prompt \
    --input_file src/data/input/complex_questions.txt \
    --output_file src/data/output/simplify.txt \
    --engine text-davinci-002 \
    --num_gen 2