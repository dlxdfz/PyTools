import logging
import sys

#formatter = logging.Formatter("%(asctime)s [%(module)s] [%(levelname)s] %(message)s")
formatter = logging.Formatter("%(asctime)s[%(module)s][%(funcName)s][%(lineno)d][%(levelname)s] %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger("post_process")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    logger.warning("warning")
    logger.info("info")
    logger.debug("debug")

