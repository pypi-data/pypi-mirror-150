import subprocess
from functools import cache
import os, re
from pathlib import Path


@cache
def get_brew_shellenv() -> dict[str, str]:
    """
	Get the output of the command: brew shellenv
	run with subprocess.run()
	"""
    export_env_var_commands: list[str] = subprocess.run(
        ['brew', 'shellenv'], stdout=subprocess.PIPE,
        universal_newlines=True).stdout.splitlines()
    env_dict = {}
    for command in export_env_var_commands:
        match = re.fullmatch(
            r'''export (?P<env_var>[A-Z_]+)="(?P<value>[^";\s]+)";''', command)
        assert match is not None
        env_dict[match.group('env_var')] = match.group('value')
    return env_dict


# export HOMEBREW_PREFIX="/usr/local"; -> /usr/local
def get_brew_env_var(env_var: str) -> str:
    """
	Get the value of a brew environment variable.
	"""
    value = os.environ.get(f"HOMEBREW_{env_var}")
    if value is None:
        value = get_brew_shellenv()[env_var]
    if not value:
        raise ValueError(
            f"Could not find value for environment variable: {env_var}")
    return value
