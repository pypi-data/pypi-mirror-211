from .__constant import *
from .__plugin import *
from .__core import *

del __constant
del __plugin
del __core

VERSION = '0.0.7'

__all__ = ('FUNC', 'TYPE', 'Info', 'PluginBase', 'Ohmytmp')
