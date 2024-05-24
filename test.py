# import logging
# from rich.logging import RichHandler

# FORMAT = "%(message)s"
# logging.basicConfig(
#     level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
# )

# log = logging.getLogger("rich")
# log.info("Hello, World!")


import logging
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("rich")

log.info("123313131")
try:
    print(1 / 0)
except Exception:
    log.exception("unable print!")