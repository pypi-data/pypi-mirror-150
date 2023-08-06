# isort: skip_file

from dishpill import error
from dishpill.version import VERSION as __version__

from dishpill.core import (
    Env,
    Wrapper,
    ObservationWrapper,
    ActionWrapper,
    RewardWrapper,
)
from dishpill.spaces import Space
from dishpill.envs import make, spec, register
from dishpill import logger
from dishpill import wrappers
import os
import sys

__all__ = ["Env", "Space", "Wrapper", "make", "spec", "register"]

# Initializing pygame initializes audio connections through SDL. SDL uses alsa by default on all Linux systems
# SDL connecting to alsa frequently create these giant lists of warnings every time you import an environment using
#   pygame
# DSP is far more benign (and should probably be the default in SDL anyways)

if sys.platform.startswith("linux"):
    os.environ["SDL_AUDIODRIVER"] = "dsp"

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
