# =============================================================================
# *   CRAPPY BUILD SCRIPT (TM)                                                *
# *      v0.1.11                                                              *
# *      @author mossffe                                                      *
# =============================================================================

import platform
import os
import sys

match platform.system():
    case "Linux":
        crappy_module = os.path.expanduser("~/.config/nvim/scripts/")
        sys.path.append(crappy_module)
    case "Windows":
        crappy_module = os.path.expanduser("%USERPROFILE%/Local/nvim/scripts/")
        sys.path.append(crappy_module)

import crappy  # noqa
from crappy import Task  # noqa
from crappy import MasterSlaveEvent  # noqa

config = crappy.config.Config()
config.argv = sys.argv
config.self_script_path = os.path.realpath(__file__)

config.task_queue = [
]

config.command_queue = [
]

crappy.driver(config)
