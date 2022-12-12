# Improving Semantic Parsing Using LLMs

## Setup

Install required packages
```bash
pip install -r requirements.txt
```

Setup GPT-3. Find the secret OpenAI API key from [this](https://beta.openai.com/account/api-keys) page. Run `export OPENAI_API_KEY=<your OpenAI API key>` in your terminal.

Prepare the semantic parse by following the instructions under src/semantic_parse/README.md

## Generate GPT-3 Input Questions

Use `src/utils/gen_gpt_input.py` to generate the questions that GPT-3 will take as input. This can be run as:

```bash
python src/utils/gen_gpt_input.py  \
    --input <groundtruth.json> \
    --output_file <gpt3_input.json> \[--use_thingtalk]
```

groudtruth.json: Groundtruth JSON for fewshot/dev/test
gpt3_input.json: Output JSON of questions, parsed ThingTalk, and answers that will be used as GPT-3 input
use_thingtalk: Whether to generate ThingTalk-based questions

### Run GPT-3

Use `src/generator.py` to run GPT-3 with specified prompt and question inputs This can be run as:

```bash
python src/generator.py \
    --prompt_template_file <prompt.prompt> \
    --input_file <gpt3_input.json> \
    --output_file <gpt3_output.json> \
    [--use_thingtalk]
```

prompt.prompt: GPT-3 prompt file
gpt3_input.json: Output JSON of questions, parsed ThingTalk, and answers that will be used as GPT-3 input
gpt3_output.json: JSON of questions and corresponding paraphrases
use_thingtalk: Whether to generate ThingTalk-based questions
There are additional flags for GPT-3 parameters that can be configured. See `src/generator.py` details

### Generate Answer

Update the filepaths in `src/semantic_parse/index.js` and run `node index.js` to generate answers to the GPT-3 paraphrases

### Evaluate

Use `src/utils/eval.py` to run GPT-3 with specified prompt and question inputs This can be run as:

```bash
python src/utils/eval.py \
    --input_file <answer.json> \
    --baseline_file <baseline_answer.json>\
    --twoshot
```

answer.json: JSON of question and semantic parser output for the semantic parse output
baseline_answer.json: JSON of question and semantic parser output for the baseline
twoshot: Whether to calculate one-shot or two-shot accuracy

### Example

The file `runfiles\full_pipelin.sh` contains examples of running each of these steps.