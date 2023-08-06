"""E3SM Kernel generation module"""

import os, subprocess, json, shutil

from microapp import appdict

from microapp import App
from ekea.utils import xmlquery

# TODO: split functions
# TODO: apply to varwhere
# TODO: debug at summit
# TODO: update doc
# TODO: write paper

here = os.path.dirname(os.path.abspath(__file__))

# E3SM app
class E3SMKernel(App):
    """Generate E3SM kernel

    Command-line arguments
    -----------------------
    casedir : str
        E3SM case directory
    callsitefile : str
        E3SM source file containing ekea kernel extraction directives
    outdir: str, optional
        E3SM kernel output directory
"""

    def __init__(self, mgr):

        self.add_argument("casedir", metavar="casedir", help="E3SM case directory")
        self.add_argument("callsitefile", metavar="callsitefile", help="ekea callsite Fortran source file")
        self.add_argument("-o", "--outdir", type=str, help="output directory")
        self.add_argument("-m", "--mpidir", type=str, help="MPI root directory")

        # placeholder for providing next application with analysis object. Not used yet.
        self.register_forward("data", help="json object")

    # main entry
    def generate(self, args, excludefile):
        """Generate E3SM kernel

        Parameters 
        -----------------------
        args : ArgParser
            MicroApp command-line parser object
        excludefile : str
            INI-format file that contains list of identifies that will be skipped during source code analysis.
"""

        # generate several absolute paths
        casedir = os.path.abspath(os.path.realpath(args.casedir["_"]))
        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        #csdir, csfile = os.path.split(callsitefile)
        #csname, csext = os.path.splitext(csfile)
        outdir = os.path.abspath(os.path.realpath(args.outdir["_"])) if args.outdir else os.getcwd()

        # create E3SM commands to clean/build/submit a E3SM case
        cleancmd = "cd %s; ./case.build --clean-all" % casedir
        buildcmd = "cd %s; ./case.build" % casedir
        runcmd = "cd %s; ./case.submit" % casedir

        # creat batch option to force wait until the job finish
        batch = xmlquery(casedir, "BATCH_SYSTEM", "--value")

        if batch == "lsf":
            runcmd += " --batch-args='-K'"

        elif "slurm" in batch:
            runcmd += " --batch-args='-W'"

        elif batch == "pbs": # SGE PBS
            runcmd += " --batch-args='-sync yes'"
            #runcmd += " --batch-args='-Wblock=true'" # PBS

        elif batch == "moab":
            runcmd += " --batch-args='-K'"

        else:
            raise Exception("Unknown batch system: %s" % batch)
 
        # create some output names
        compjson = os.path.join(outdir, "compile.json")
        outfile = os.path.join(outdir, "model.json")
        srcbackup = os.path.join(outdir, "backup", "src")

        # get mpi root directory
        if args.mpidir:
            mpidir = os.path.abspath(os.path.realpath(args.mpidir["_"]))

        else:
            mpidir = os.environ["MPI_ROOT"]

        blddir = xmlquery(casedir, "OBJROOT", "--value")
        if not os.path.isfile(compjson) and os.path.isdir(blddir):
            shutil.rmtree(blddir)

        # run a fortlab command to compile e3sm and collect compiler options
        cmd = " -- buildscan '%s' --savejson '%s' --reuse '%s' --backupdir '%s'" % (
                buildcmd, compjson, compjson, srcbackup)
        ret, fwds = self.manager.run_command(cmd)

        # save compjson with case directory map
        # handle mpas converted file for callsitefile2
        # TODO: replace ekea contaminated file with original files
        # TODO: recover removed e3sm converted files in cmake-bld, ... folders

        # copy source file back to original locations if deleted
        with open(compjson) as f:
            jcomp = json.load(f)

            for srcpath, compdata in jcomp.items():
                srcbackup = compdata["srcbackup"]

                if not srcbackup:
                    continue

                if not os.path.isfile(srcpath) and srcbackup[0] and os.path.isfile(srcbackup[0]):
                    orgdir = os.path.dirname(srcpath)

                    if not os.path.isdir(orgdir):
                        os.makedirs(orgdir)

                    shutil.copy(srcbackup[0], srcpath)

                for incsrc, incbackup in srcbackup[1:]:
                    if not os.path.isfile(incsrc) and incbackup and os.path.isfile(incbackup):
                        orgdir = os.path.dirname(incsrc)

                        if not os.path.isdir(orgdir):
                            os.makedirs(orgdir)

                        shutil.copy(incbackup, incsrc)

        # Run microapp command to analize source files, to generate timing raw data, and generate kernel and input data files.
        self.execute(mpidir, compjson, excludefile, callsitefile, outdir, buildcmd, runcmd, outfile, )

    def execute(self):
                
        statedir = os.path.join(outdir, "state")
        etimedir = os.path.join(outdir, "etime")

        if os.path.isdir(statedir) and os.path.isfile(os.path.join(statedir, "Makefile")):
            stdout = subprocess.check_output("make recover", cwd=statedir, shell=True)

        elif os.path.isdir(etimedir) and os.path.isfile(os.path.join(etimedir, "Makefile")):
            stdout = subprocess.check_output("make recover", cwd=etimedir, shell=True)

        # fortlab command to analyse source files
        rescmd = (" -- resolve --mpi header='%s/include/mpif.h' --openmp enable"
                 " --compile-info '%s' --exclude-ini '%s' '%s'" % (
                mpidir, compjson, excludefile, callsitefile))

        # fortlab command to generate raw timing data
        cmd = rescmd + " -- runscan '@analysis' -s 'timing' --outdir '%s' --buildcmd '%s' --runcmd '%s' --output '%s'" % (
                    outdir, buildcmd, runcmd, outfile)

        # fortlab command to generate kernel and input/output data
        cmd = cmd + " -- kernelgen '@analysis' --model '@model' --repr-etime 'ndata=40,nbins=10'  --outdir '%s'" % outdir

        # run microapp command
        ret, fwds = self.manager.run_command(cmd)
