#!/usr/bin/env python

from Gaugi import LoggingLevel
from Gaugi import ToolSvc, GeV

from kepler.core import ElectronLoop
from kepler.core.enumerators import Dataframe as DataframeEnum

import argparse
import sys,os

parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

#
# job configuration
#

parser.add_argument('-i','--inputFiles', action='store',
    dest='inputFiles', required = True, nargs='+',
    help = "The input files.")

parser.add_argument('-o','--outputFile', action='store',
    dest='outputFile', required = False, default = None,
    help = "The output name.")

parser.add_argument('-n','--nov', action='store',
    dest='nov', required = False, default = -1, type=int,
    help = "Number of events.")

parser.add_argument('-p','--path', action='store',
    dest='path', required = False, default='*/HLT/Physval/Egamma/probes', type=str,
    help = "Ntuple base path.")

parser.add_argument('-l','--level', action='store',
    dest='level', required = False, type=str, default='INFO',
    help = "VERBOSE/INFO/DEBUG/WARNING/ERROR/FATAL")

parser.add_argument('--mute', action='store_true',
    dest='mute', required = False, 
    help = "Use this for production. quite output")


#
# event selection configuration
#

parser.add_argument('--et_bins', action='store',
    dest='et_bins', required = False, type=str, default='"[15.0, 20.0, 30.0, 40.0, 50.0, 100000]"',
    help = "et bin ranges")
    
parser.add_argument('--eta_bins', action='store',
    dest='eta_bins', required = False, type=str, default='"[0.0, 0.8, 1.37, 1.54, 2.37, 2.50]"',
    help = "eta bin ranges")

parser.add_argument('--pidname', action='store',
    dest='pidname', required = False, type=str, default='el_lhvloose',
    help = "Offline pid cut.") 

parser.add_argument('--et_min', action='store',
    dest='et_min', required = False, type=int, default=0,
    help = "Fast calo min et value in GeV.") 

parser.add_argument('--et_max', action='store',
    dest='et_max', required = False, type=int, default=1000,
    help = "Fast calo max et value in GeV") 

parser.add_argument('-t','--target_label', action='store',
    dest='target_label', required = False, default = 1, type=int,
    help = "Additional target label to be stored")

parser.add_argument('--add_tdt_triggers', action='store_true',
    dest='add_tdt_triggers', required = False, 
    help = "Include trigges from TDT into the data samples")


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()



acc = ElectronLoop(  "EventATLASLoop",
                     inputFiles = args.inputFiles,
                     treePath   = eval(args.path),
                     dataframe  = DataframeEnum.Electron_v1,
                     outputFile = args.outputFile,
                     level      = getattr(LoggingLevel, args.level),
                     mute_progressbar = args.mute,
                  )


class IsoDecorator:
    def __init__(self):
        from kepler.emulator.TrigEgammaPrecisionElectronHypoTool import configure
        self.tool = configure('isolation', 'lhtight', 'ivarloose')
        self.tool.initialize()
    def __call__(self, ctx):
        # online container can have more than one element
        elCont = ctx.getHandler("HLT__ElectronContainer")
        return [ (el.accept("trig_EF_el_lhtight") and self.tool.isolation(el)) for el in elCont]

iso_decorator = IsoDecorator()

def deltaR_decorator( ctx ):
    # container with only one element
    el = ctx.getHandler("ElectronContainer")
    return el.deltaR()

def eeMass_decorator( ctx ):
    el = ctx.getHandler("ElectronContainer")
    return el.eeMass()



class MyFilter:
    def __init__ ( self, etmin, etmax, pidname ):
        self.etmin = etmin
        self.etmax = etmax
        self.pidname = pidname

    def __call__(self, context):
        elCont = context.getHandler( "ElectronContainer" )
        fc = context.getHandler( "HLT__TrigEMClusterContainer" )

        if '!' in self.pidname:
            if elCont.accept(self.pidname.replace("!","") ) :
                #print('reproved by veto offline pid %s', self.pidname)
                return False 
        else:
            if not elCont.accept(self.pidname):
                #print('reproved by offline pid '+self.pidname)
                return False
        if elCont.et() < 2*GeV:
            #print('reproved by 2 GeV offline et cut.')
            return False
        if not fc.isGoodRinger():
            #print('reproved by isGoodRinger condition.')
            return False
        if not ( (fc.et() >= self.etmin*GeV) and (fc.et() < self.etmax*GeV ) ):
            #print('reproved by fast calo energy range.')
            return False

        return True

my_filter = MyFilter(args.et_min, args.et_max, eval(args.pidname))


from kepler.menu.install import install_commom_features_for_electron_dump
extra_features = install_commom_features_for_electron_dump() 

if args.add_tdt_triggers:
    original_triggers = [ "TDT__L1Calo__e28_lhtight_nod0_ivarloose",
                          "TDT__L2Calo__e28_lhtight_nod0_ivarloose",
                          "TDT__L2__e28_lhtight_nod0_ivarloose",
                          "TDT__EFCalo__e28_lhtight_nod0_ivarloose",
                          "TDT__HLT__e28_lhtight_nod0_ivarloose",
                          "TDT__L1Calo__e28_lhtight_nod0_noringer_ivarloose",
                          "TDT__L2Calo__e28_lhtight_nod0_noringer_ivarloose",
                          "TDT__L2__e28_lhtight_nod0_noringer_ivarloose",
                          "TDT__EFCalo__e28_lhtight_nod0_noringer_ivarloose",
                          "TDT__HLT__e28_lhtight_nod0_noringer_ivarloose",
                        ]
    extra_features += original_triggers



#
# Initial filter
#

from kepler.filter import Filter
filter = Filter( "Filter", [my_filter])
ToolSvc+=filter



#
# Electron dumper
#
from kepler.dumper import ElectronDumper
output = args.outputFile.replace('.root','')

et_bins = eval(eval(args.et_bins))
eta_bins = eval(eval(args.eta_bins))


dumper = ElectronDumper("Dumper", output, et_bins, eta_bins, dumpRings=True, target=args.target_label)
# append extra features from emulator
dumper += extra_features

# append extra features by hand!
dumper.decorate( "trig_EF_el_lhtight_ivarloose", iso_decorator )
dumper.decorate( "el_TaP_Mass", eeMass_decorator)
dumper.decorate( "el_TaP_deltaR", deltaR_decorator)

ToolSvc+=dumper

acc.run(args.nov)


