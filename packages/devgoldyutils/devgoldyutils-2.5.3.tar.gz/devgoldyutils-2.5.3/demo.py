import logging as log
from dataclasses import dataclass, field
from devgoldyutils import add_custom_handler, DictDataclass, Colors, DictClass, short_str

logger = add_custom_handler(log.getLogger("uwu"), level=log.DEBUG)

print(short_str("jassim is amazing at programming", 10))