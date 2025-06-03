from omegaconf import DictConfig


def load_hydra_config(config_path="../../config", config_name="config.yaml") -> DictConfig:
    from hydra import compose, initialize
    from hydra.core.global_hydra import GlobalHydra

    if GlobalHydra.instance().is_initialized():
        GlobalHydra.instance().clear()

    with initialize(version_base=None, config_path=config_path):
        # 함수형 태스크의 인자로 전달 하려면 dict 변환 필요
        # return OmegaConf.to_container(cfg, resolve=True)
        return compose(config_name=config_name)
