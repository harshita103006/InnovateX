import math
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Small LM for perplexity (lightweight)
_MODEL_NAME = "distilgpt2"

_tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)
_model = AutoModelForCausalLM.from_pretrained(_MODEL_NAME)
_model.eval()

@torch.no_grad()
def compute_perplexity(text: str) -> float:
    if not text.strip():
        return float("inf")

    enc = _tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    input_ids = enc["input_ids"]

    outputs = _model(input_ids, labels=input_ids)
    loss = float(outputs.loss)
    ppl = math.exp(loss) if loss < 50 else float("inf")
    return round(ppl, 3)
