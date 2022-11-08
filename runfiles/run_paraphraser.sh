python src/generator.py \
		--prompt_template_file src/data/prompts/paraphrase.prompt \
		--input_file src/data/input/simple_questions.txt \
		--output_file src/data/output/paraphrase.txt \
        --engine text-davinci-002 \
        --num_gen 2