
__all__ = ['ElectronSequence']

from Gaugi import Logger
from Gaugi.macros import *
from Gaugi import GeV

import pandas as pd
import numpy as np

from kepler.menu import get_chain_dict

from collections import OrderedDict
from pprint import pprint
from pandarallel import pandarallel
pandarallel.initialize()


#
# Electron sequence used during Run 2
#
class ElectronSequence(Logger):

    # NOTE: etcut triggers not supported yet
    #
    # chain = Chain("HLT_e28_lhtight_nod0_ringer_v8_ivarloose", "HLT_e28_lhtight_nod0_ivarloose", 
    #                L1Seed = 'L1_EM22VHI', l2calo_column = 'ringer_tight_v8')
    #
    def __init__(self, trigger, 
                 L1Seed = None, 
                 l2calo_etthr = None,
                 l2calo_column = None,
                 l2_column = None,
                 efcalo_etthr = None,
                 hlt_etthr = None,
                 hlt_column = None,
                ):

        Logger.__init__(self)

        # Configure values
        self.L1Seed_column = L1Seed
        self.l2calo_column = l2calo_column
        self.l2_column = l2_column
        self.hlt_column = hlt_column
        # energy cut
        self.l2calo_etthr = l2calo_etthr
        self.efcalo_etthr = efcalo_etthr
        self.hlt_etthr = hlt_etthr
        self.trigger = trigger

        # configure my sequence
        self.configure()


    #
    # Configure all missing parameters for the Run 2 electron sequence
    #
    def configure(self):

        d = get_chain_dict(self.trigger)

        etthr = d['etthr']
        pidname = d['pidname']
        iso = d['iso']

        if not self.L1Seed_column:
            self.L1Seed_column = d['L1Seed']

        # configure fast calo cluster energy cut - 3 GeV
        if not self.l2calo_etthr:
            self.l2calo_etthr = (etthr - 3) * GeV


        # configure as noringer version
        if not self.l2calo_column or 'noringer' in self.trigger:
            if etthr >= 0 and etthr < 12:
                self.l2calo_column = 'trig_L2_cl_%s_et0to12' % (pidname.replace('lh',''))
            elif etthr >= 12 and etthr < 22:
                self.l2calo_column = 'trig_L2_cl_%s_et12to22' % (pidname.replace('lh',''))
            else: # etthr >= 22
                self.l2calo_column = 'trig_L2_cl_%s_et22toInf' % (pidname.replace('lh',''))


        # configure fast electron step
        if not self.l2_column:
            if etthr >= 0 and etthr < 15:
                self.l2_column = 'trig_L2_el_cut_pt0to15' 
            elif etthr >= 15 and etthr < 20:
                self.l2_column = 'trig_L2_el_cut_pt15to20' 
            elif etthr >= 20 and etthr < 50:
                self.l2_column = 'trig_L2_el_cut_pt20to50' 
            else:
                self.l2_column = 'trig_L2_el_cut_pt50toInf' 


        # configure precision calo et cut
        if not self.efcalo_etthr:
            self.efcalo_etthr = etthr * GeV

        if not self.hlt_etthr:
            self.hlt_etthr = etthr * GeV

        if not self.hlt_column:
            self.hlt_column = 'trig_EF_el_%s' % pidname
            if iso: # add isolation suffix
                self.hlt_column+='_'+iso

        #MSG_DEBUG(self, "Chain name: %s", self.trigger)
        pprint ( OrderedDict( {
                'L1Seed' : self.L1Seed_column,
                'L2Calo' : (self.l2calo_etthr, self.l2calo_column),
                'L2'     : self.l2_column,
                'EFCalo' : self.efcalo_etthr,
                'HLT'    : (self.hlt_etthr, self.hlt_column)
        }) )


    def __apply(self, row):
        l1calo_passed=False; l2calo_passed=False; l2_passed=False; efcalo_passed=False; hlt_passed=False
        if row[self.L1Seed_column]:
            l1calo_passed=True
            if (row['trig_L2_cl_et'] >= self.l2calo_etthr) and (row[self.l2calo_column] == True):
                l2calo_passed=True
                if row[self.l2_column]:
                    l2_passed=True
                    if row['trig_EF_cl_et'] >= self.efcalo_etthr:
                        efcalo_passed=True
                        if row[self.hlt_column] and (row['trig_EF_el_et'] >= self.hlt_etthr):
                            hlt_passed=True
        return l1calo_passed,l2calo_passed,l2_passed,efcalo_passed,hlt_passed
     



    def apply(self, df):

        col_name = self.trigger.replace('HLT_','')

        # append new columns into the dataframe
        df['L1Calo_'+col_name ] = False
        df['L2Calo_'+col_name ] = False
        df['L2_'+col_name ]     = False
        df['EFCalo_'+col_name ] = False
        df['HLT_'+col_name ]    = False

        MSG_DEBUG(self, "Number of events   : %d", df.shape[0])

        # copy some columns to not allocate too much memory
        df_temp = df[[self.L1Seed_column, self.l2calo_column, 'trig_L2_cl_et', self.l2_column, 
                     'trig_EF_cl_et', 'trig_EF_el_et', self.hlt_column]]


        # Filter by L1
        df_temp = df_temp.loc[df_temp[self.L1Seed_column] == True]
        # store decisions
        df.at[df_temp.index, 'L1Calo_' + col_name] = True
        MSG_DEBUG(self, "Approved by L1     : %d", df_temp.shape[0])


        # Filter by L2Calo
        df_temp = df_temp.loc[ (df_temp['trig_L2_cl_et'] >= self.l2calo_etthr) & (df_temp[self.l2calo_column] == True)]
        # store decisions
        df.at[df_temp.index, 'L2Calo_' + col_name] = True
        MSG_DEBUG(self, "Approved by L2Calo : %d", df_temp.shape[0])


        # Filter L2 electron
        df_temp = df_temp.loc[ (df_temp[self.l2_column] == True) ]
        df.at[df_temp.index, 'L2_' + col_name] = True
        MSG_DEBUG(self, "Approved by L2     : %d", df_temp.shape[0])


        # Filter EF Calo
        df_temp = df_temp.loc[ (df_temp['trig_EF_cl_et'] >= self.efcalo_etthr) ]
        df.at[df_temp.index, 'EFCalo_' + col_name] = True
        MSG_DEBUG(self, "Approved by EFCalo : %d", df_temp.shape[0])


        # Filter HLT
        df_temp = df_temp.loc[ (df_temp[self.hlt_column] == True) & (df_temp['trig_EF_el_et'] >= self.hlt_etthr) ]
        df.at[df_temp.index, 'HLT_' + col_name] = True
        MSG_DEBUG(self, "Approved by HLT    : %d", df_temp.shape[0])
