# -*- coding:utf-8 -*-

from .OpenApi import OpenApi
from .Winmail import Winmail
from .utils import start_winmail_service, stop_winmail_service

__all__ = ["OpenApi", "Winmail", "start_winmail_service", "stop_winmail_service"]

import os
if os.name == "nt":
    from .ComApi import ComApi
    
    __all__.append("ComApi")