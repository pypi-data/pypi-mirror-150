"""MPAS Ocean kernel generation module."""

import os, subprocess, json, shutil

from microapp import appdict

from ekea.e3smapp import E3SMKernel, here
from ekea.utils import xmlquery

# MPAS Ocean app
class MPASOcnKernel(E3SMKernel):
    """A wrapper class of E3SMKernel to place any customization for MPAS Ocean.
    """

    _name_ = "mpasocn"
    _version_ = "1.0.0"

    # The main entry to extract a MPAS Ocean kernel.
    def perform(self, args):
        """Extract a MPAS Ocean kernel."""

        # MPAS Ocean convert raw source files before the compilation
        # Following statements convert the path to the raw source file to
        # the path to the converted sourcefile.

        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        csdir, csfile = os.path.split(callsitefile)
        reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-source", "src"))
        callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", reldir, "%s.f90" % csname)

        args.callsitefile["_"] = callsitefile2

        self.generate(args, "exclude_e3sm_mpas.ini")

