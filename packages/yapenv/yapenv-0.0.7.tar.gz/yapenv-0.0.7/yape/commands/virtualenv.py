import os
from yape.log import yape_log
from yape.utils import run_python_module, option_or_empty, clean_args
from yape.config import YAPEConfig


def virtualenv_args(config: YAPEConfig):
    """Returns the virtualenv args from the yape config

    Args:
        config (YAPEConfig): The yape config.
    """
    return clean_args(
        *option_or_empty("--python", config.python_executable or config.python_version),
        *config.venv_args,
        config.venv_path,
    )


def virtualenv_create(config: YAPEConfig):
    """Create a virtualenv given the yape config.

    Args:
        config (YAPEConfig): The yape config.
    """
    yape_log.info("Creating virtualenv @ " + config.venv_path)
    cmnd = ["virtualenv", *virtualenv_args(config)]
    yape_log.debug(str(cmnd))
    run_python_module(*cmnd, use_vevn=False)

    if config.pip_config_path is not None:
        config_path = config.resolve_from_source_directory(config.pip_config_path)
        if not os.path.isfile(config_path):
            yape_log.warn("Could not set custom config path, pip_config_path not found @ " + config_path)
        else:
            os.symlink(config_path, config.resolve_from_venv_directory("pip.conf"))
