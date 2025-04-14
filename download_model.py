import json
import torch
from transformers import AutoModelForCausalLM

def main():
    with open("conf/config.json", "r") as config:
        cfg = json.load(config)

    model = AutoModelForCausalLM.from_pretrained(
        cfg.model,
        torch_dtype=torch.bfloat16,
        device_map=None
    ).to("cpu")

    model.save_pretrained("./models")
