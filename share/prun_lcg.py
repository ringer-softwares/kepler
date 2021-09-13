#!/usr/bin/env python3

from Gaugi.messenger import LoggingLevel, Logger
from Gaugi.messenger.macros import *
from pprint import pprint
import argparse


logger = Logger.getModuleLogger("prometheus.prun.lcg")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('--inDS', action='store',  dest='inDS', required = True, 
    help = "The dataset input file")

parser.add_argument('--outDS', action='store',  dest='outDS', required = True,
    help = "The dataset input file")

parser.add_argument('-c','--command', action='store', 
    dest='command', required = True,
    help = "The command job")

parser.add_argument('--containerImage', action='store', 
    dest='containerImage', required = False, default = "docker://jodafons/prometheus:lcg",
    help = "The docker container image")

parser.add_argument('--nFilesPerJob', action='store', type=int, default=1,
    dest='nFilesPerJob', required = False,
    help = "The number of files per job.")

parser.add_argument('--site', action='store' , default='AUTO',
    dest='site', required = False,
    help = "The site name")

parser.add_argument('--dry_run', action='store_true' ,
    dest='dry_run', required = False,
    help = "Dry run")

parser.add_argument('--outputs', action='store' ,
    dest='outputs', required = True,
    help = "Something like 'output:output.root'")





import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()


# treat the command
job_command = args.command


if not '%IN' in job_command:
  logger.fatal( "You must include the %IN in the job command to reference it as input (e.g -i %IN)." )




command = """ prun --exec \
       "sh -c '. /setup_envs.sh && {COMMAND}';" \
     --excludedSite=ANALY_DESY-HH_UCORE,ANALY_MWT2_SL6,ANALY_MWT2_HIMEM,ANALY_DESY-HH,ANALY_FZK_UCORE,ANALY_FZU,DESY-HH_UCORE,FZK-LCG2_UCORE,CERN-T0 \
     --containerImage={CONTAINER} \
     --noBuild \
     --inDS={INDS} \
     --outDS={OUTDS} \
     --disableAutoRetry \
     --outputs="{OUTPUTS}" \
     --nFilesPerJob={N_FILES_PER_JOB} \
     --forceStaged \
     --site {SITE} \
     --mergeOutput \
    """

command = command.format( CONTAINER = args.containerImage,
                            INDS      = args.inDS,
                            OUTDS     = args.outDS,
                            COMMAND   = job_command,
                            N_FILES_PER_JOB = args.nFilesPerJob,
                            SITE      = args.site,
                            OUTPUTS   = args.outputs,
                            )

logger.info(command)
print(command)


if not args.dry_run:
  os.system(command)



