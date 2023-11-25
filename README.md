## Setup

* Copy `.env.template` to `.env` and enter your keys (notably OPENAI_API_KEY).
* `pip install requirements.txt` and optionally `requirements.dev.txt`

## Use

```
python evaluate.py <optional arguments>
```

By default, this will run an evaluation with gpt-3.5-turbo on all 100 samples in the Misconceptions category of TruthfulQA.

To specify model, supply `--model <name>` using the [LiteLLM naming](https://docs.litellm.ai/docs/providers).

To make a shorter test run, supply `--num-samples <count>`.

To see the generated answer to every question, add `--verbose`.

Example:

```
python evaluate.py model=gpt-4-1106-preview num-samples=3 --verbose
```

More options: `python evaluate.py --help`.
