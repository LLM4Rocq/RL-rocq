import re
import hydra
from hydra.core.hydra_config import HydraConfig
import torch
from omegaconf import DictConfig, OmegaConf
from openai.types.chat import ChatCompletionMessage as Response
from transformers import AutoTokenizer, AutoModelForCausalLM
from trl import GRPOConfig, GRPOTrainer

import prompt
import agent
import data
import language

def format_reward_func(completions: list[list[Response]], **kwargs):
    """ Reward function that checks if completions respect a specific format. """
    pattern = r"^<think>.*?</think><proof>.*?</proof>$"
    responses = [completion[0]["content"] for completion in completions]
    matches = [re.match(pattern, content) for content in responses]
    return [1.0 if match else 0.0 for match in matches]

def itype_check_reward_func(interface: language.Interface, completions: list[list[Response]], **kwargs):
    """ Reward function that checks if completions type check. """
    responses = [c[0]['content'] for c in completions]
    proofs = [agent.extract_proof(r) for r in responses]

    rewards = []
    for proof in proofs:
        if proof:
            res = interface.type_check(proof)
            if res.is_error():
                rewards.append(0.0)
            else:
                rewards.append(1.0)
        else:
            rewards.append(0.0)
    return rewards

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):

    # Language interface
    hydra_cfg = HydraConfig.get()
    hydra_cfg = OmegaConf.to_container(hydra_cfg.runtime.choices)
    match hydra_cfg["language"]:
        case "rocq":
            interface = language.RocqInterface(**cfg.language)
        case _:
            return "ERROR: wrong language name"

    # Dataset
    dataset = data.dataset
    dataset = [prompt.make_prompt(thm_data) for thm_data in dataset]
    dataset = [{'prompt': p} for p in dataset]

    # Training
    training_args = GRPOConfig(**cfg.training_args)

    model = AutoModelForCausalLM.from_pretrained(
        cfg.model,
        torch_dtype=torch.bfloat16,
        device_map=None
    ).to("cpu")

    tokenizer = AutoTokenizer.from_pretrained(cfg.model)
    tokenizer.pad_token = tokenizer.eos_token

    def type_check_reward_func(completions: list[list[Response]], **kwargs):
        return itype_check_reward_func(interface, completions, **kwargs)

    trainer = GRPOTrainer(
        model=model,
        processing_class=tokenizer,
        reward_funcs=[
            format_reward_func,
            type_check_reward_func
        ],
        args=training_args,
        train_dataset=dataset,
        #peft_config=peft_config
    )

    print("Start training ...")
    trainer.train()

if __name__ == "__main__":
    main()
