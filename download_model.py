import torch
import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf
from transformers import AutoTokenizer, AutoModelForCausalLM

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    AutoModelForCausalLM.from_pretrained(
        cfg.model,
        torch_dtype=torch.bfloat16,
        device_map=None
    ).to("cpu")
