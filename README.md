## Setup

* Copy `.env.template` to `.env` and enter your keys (notably OPENAI_API_KEY).
* `pip install requirements.txt` and optionally `requirements.dev.txt`

## Use

```
python main.py <optional arguments>
```

By default, this will run an evaluation with gpt-3.5-turbo on all 100 samples in the Misconceptions category of TruthfulQA.

To specify model, supply `--model <name>` using the [LiteLLM naming](https://docs.litellm.ai/docs/providers).

To make a shorter test run, supply `--num_samples <count>`.

Example:

```
python main.py model=gpt-4-1106-preview num_samples=3
```

More options: `python main.py --help`.
