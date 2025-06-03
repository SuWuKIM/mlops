import os

from omegaconf import OmegaConf, DictConfig


def load_config(config_path: str) -> DictConfig:
    return OmegaConf.load(config_path)


def load_bento_config(bento_file: str) -> DictConfig | None:
    try:
        current_dir = os.path.dirname(os.path.abspath(bento_file))
        return load_config(os.path.join(current_dir, "config.yaml"))
    except FileNotFoundError:
        return None
