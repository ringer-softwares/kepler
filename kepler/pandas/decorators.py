
__all__ = [ 
            'RingerDecorator',
           ]

from Gaugi import Logger
from Gaugi.macros import *
from Gaugi import GeV

import pandas as pd
import numpy as np
import os

from kepler.emulator.hypos import load_models


#
# Class responsible to propagate the ringer decision throut the pandas frame and append the decision and output
#
class RingerDecorator(Logger):

    #
    # Constructor
    #
    def __init__( self, column, path, generator , 
                  et_column = 'trig_L2_cl_et', 
                  eta_column = 'trig_L2_cl_eta',
                  batch_size = 1024,
                  verbose=True):

        Logger.__init__(self)
        self.path = path
        # function to prepare data input
        self.generator = generator
        self.column = column
        self.et_column = et_column
        self.eta_column = eta_column
        self.batch_size = batch_size
        self.verbose = verbose
        # configure 
        self.configure()


    #
    # Load the tuning
    #
    def configure(self):
        MSG_INFO(self, 'Reading... %s', self.path)
        self.__core, _ = load_models(self.path)
        self.etbins = self.__core['model_etBins']
        self.etabins = self.__core['model_etaBins']
        self.etbins_thr = self.__core['threshold_etBins']
        self.etabins_thr = self.__core['threshold_etaBins']
        self.models = self.__core['models']
        self.thresholds = self.__core['thresholds']

    #
    # Decorate the pandas dataframe with output and decision and store into self.column
    #
    def apply(self, df, batch_size=2048):

        df[self.column+'_output'] = np.nan
        df[self.column] = np.nan

        # Get L2 values
        et = df[self.et_column].values / GeV
        eta = abs(df[self.eta_column].values)
  
        df['et_bin'] = np.digitize( et, self.etbins, right=False) - 1
        df['eta_bin'] = np.digitize( eta, self.etabins, right=False) - 1

        # Propagate the input and append the output into the dataframe
        for et_bin in df['et_bin'].unique():
            for eta_bin in df['eta_bin'].unique():
                index = df.loc[ (df['et_bin'] == et_bin) & (df['eta_bin'] == eta_bin) ].index
                if len(index)>0:
                    model = self.models[et_bin][eta_bin]
                    output = model.predict(self.generator(df.loc[ (df['et_bin'] == et_bin) & (df['eta_bin'] == eta_bin) ]), 
                                           verbose=0, batch_size=self.batch_size)
                    df.at[index, self.column+'_output'] = output

        if df[self.column+'_output'].isnull().sum():
            MSG_WARNING(self, 'There is nan values into the %s_output column. Please check!', self.column)

        #
        # Now lets take the decision using the output
        #

        df['et_bin'] = np.digitize( et, self.etbins_thr, right=False) - 1
        df['eta_bin'] = np.digitize( eta, self.etabins_thr, right=False) - 1

        # Take the decision
        for et_bin in df['et_bin'].unique():
            for eta_bin in df['eta_bin'].unique():
                df_temp = df.loc[ (df['et_bin'] == et_bin) & (df['eta_bin'] == eta_bin) ]
                if len(df_temp)>0:
                    thr       = self.thresholds[et_bin][eta_bin]
                    output    = df_temp[self.column+'_output'].values
                    avgmu     = df_temp['avgmu'].values
                    min_avgmu = thr['min_avgmu']
                    max_avgmu = thr['max_avgmu']
                    avgmu[avgmu < min_avgmu ] = min_avgmu
                    avgmu[avgmu > max_avgmu]  = max_avgmu
                    df.at[df_temp.index, self.column] = np.greater( output, (avgmu * thr['slope'] + thr['offset']) )


        if df[self.column].isnull().sum():
            MSG_WARNING(self, 'There is nan values into the %s_output column. Please check!', self.column)

        # drop temp columns
        df.drop(['et_bin', 'eta_bin'], axis=1, inplace=True)
 




