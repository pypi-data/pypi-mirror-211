import logging
import os
import tomllib


print("Path: ", os.getcwd())

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def get_values(*args: str) -> str:
    args = list(args)
    par = config
    while args:
        key = args.pop(0)
        try:
            par = par[key]
            continue
        except KeyError as e:
            logger.info(e.args[0])
            print(e.args[0])
            return "??"
    return par


with open("./config.toml", "rb") as f:
    config = tomllib.load(f)
