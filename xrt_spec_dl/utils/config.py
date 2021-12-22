from omegaconf import OmegaConf
from dataclasses import dataclass
from enum import IntEnum, Enum
from pathlib import Path


def get_path_of_user_config() -> Path:

    # if _custom_config_path is not None:

    #     config_path: Path = Path(_custom_config_path)

    config_path: Path = Path().home() / ".config" / "xrt_spec_dl"

    if not config_path.exists():

        config_path.mkdir(parents=True)

    return config_path


@dataclass
class Config:
    #    logging: Logging = Logging()
    cache_dir: str = "~/.xrt_spec_dl"
    use_cache: bool = False


# Read the default Config

xrt_spec_dl_config: Config = OmegaConf.structured(Config)


# now glob the config directory

for user_config_file in get_path_of_user_config().glob("*.yml"):

    _partial_conf = OmegaConf.load(user_config_file)

    xrt_spec_dl_config: Config = OmegaConf.merge(
        xrt_spec_dl_config, _partial_conf
    )
