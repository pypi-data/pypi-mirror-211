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


def get_enum_elements(name: str) -> dict[bytes, str]:
    """use for getting Enum.ELEMENTS"""
    e = dict()
    """return dictionary"""
    for par in get_values("DLMS", name):
        b_v: bytes = par["enum"].to_bytes()
        """value in bytes"""
        e[b_v] = par["value"]
    return e


try:
    with open("./config.toml", "rb") as f:
        config = tomllib.load(f)
except FileNotFoundError as e:
    logger.warning(e)
    config = dict()
