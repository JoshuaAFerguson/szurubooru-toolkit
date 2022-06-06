import sys

from loguru import logger

from .config import Config
from .danbooru import Danbooru  # noqa F401
from .gelbooru import Gelbooru  # noqa F401
from .saucenao import SauceNao  # noqa F401
from .szurubooru import Post  # noqa F401
from .szurubooru import Szurubooru
from .twitter import Twitter  # noqa F401
from .utils import audit_rating  # noqa F401
from .utils import collect_sources  # noqa F401
from .utils import convert_rating  # noqa F401
from .utils import download_media  # noqa F401
from .utils import get_md5sum  # noqa F401
from .utils import get_posts_from_booru  # noqa F401
from .utils import sanitize_tags  # noqa F401
from .utils import scrape_sankaku  # noqa F401
from .utils import setup_logger  # noqa F401
from .utils import shrink_img  # noqa F401
from .utils import statistics  # noqa F401


logger.remove(0)
logger.add(
    sink=sys.stderr,
    backtrace=False,
    colorize=True,
    level='ERROR',
    enqueue=True,
    diagnose=False,
    format=''.join(
        '<lr>[{level}]</lr> <lg>[{time:DD.MM.YYYY, HH:mm:ss zz}]</lg> ' '<ly>[{module}.{function}]</ly>: {message}',
    ),
)

config = Config()
if config.auto_tagger['deepbooru_enabled']:
    from .deepbooru import Deepbooru  # noqa F401

setup_logger(config)

szuru = Szurubooru(config.szurubooru['url'], config.szurubooru['username'], config.szurubooru['api_token'])
