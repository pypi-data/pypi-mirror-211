__version__ = '0.9.1'
__user_agent__ = f"E620py/{__version__} (by mrcrabs)"
base_url = 'https://e621.net'

from .api import E6Get, E6Post, ConnectionHandler
from .exceptions import *
from .objects import *
from .downloader import Downloader
