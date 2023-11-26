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

## Running Huggingface models

Oobabooga may be one of the most versatile options to serve various HF models.

### Running through Oobabooga locally

Step 1. Check out https://github.com/oobabooga/text-generation-webui

Step 2. Start the interface and go to the provided URL.

Step 3. Go into Model > Download model or LoRA > copy model name/path from HF. Click Download and wait until completed (can take a few minutes).

Step 4. Load the model. This may require figuring out the right loader. Transformers is a good start.

Step 5. Run the script with the argument `--api-url <URL>` with the above URL. This will ignore the model option. (Even if you write gpt-3 it will send them to your notebook)

### Colab with Oobabooga

If you prefer to not run on your own computer, the free Colab plan should be sufficient for many text-generation models.

You can start a server that you can connect to on Colab from this script.

Step 1. Open the following notebook: https://colab.research.google.com/github/oobabooga/text-generation-webui/blob/main/Colab-TextGen-GPU.ipynb

Step 2. Confirm that it says T4 in the upper right (or better?).

Step 3. **Before running, in the Step 2 cell, tick ☑ API and change the command_line args to `--extensions openai`**

Step 4. In the Step 2 cell, change the model_url to your preferred model.

Step 5. Run both cells.

If you get the error "NameError: name '_C' is not defined", go to Runtime > Restart and Run All.

Step 6. Wait for it to finish loading. This can take several minutes.

Step 7. Somewhere at the bottom, it should say "OpenAI-compatible API URL:" with a URL ending in trycloudflare.com. Copy this.

Step 8. Run the script with the argument `--api-url <URL>`. This will ignore the model option. (Even if you write gpt-3 it will send them to your notebook)
