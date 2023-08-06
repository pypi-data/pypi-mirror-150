"""EAM kernel generation module."""

import os, subprocess, json, shutil

from ekea.e3smapp import E3SMKernel, here
from ekea.utils import xmlquery

# EAM app
class EAMKernel(E3SMKernel):
    """A wrapper class of E3SMKernel to place any customization for EAM.
    """

    _name_ = "eam"
    _version_ = "1.0.0"

    # the main entry to extract a EAM kernel.
    def perform(self, args):
        """Extract a EAM kernel."""

        self.generate(args, "exclude_e3sm_eam.ini")
