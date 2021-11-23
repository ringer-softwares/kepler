
__all__ = [ 
            'RingerDecorator',
            'create_ringer_v8_decorators',
            'create_ringer_v8_decorators_official',
            'create_ringer_v9_decorators',
           ]

from Gaugi import Logger
from Gaugi.macros import *
from Gaugi import GeV

import pandas as pd
import numpy as np
import os

from kepler.emulator.hypos import load_ringer_models


def create_ringer_v8_decorators_official( column = 'ringer_v8_{pidname}'):

    basepath = os.environ['RINGER_CALIBPATH'] + '/models/Zee/TrigL2_20180125_v8'
    
    def generator( df ):
        columns= ['trig_L2_cl_ring_%d'%i for i in range(100)]
        rings = df[columns].values.astype(np.float32)
        def norm1( data ):
            norms = np.abs( data.sum(axis=1) )
            norms[norms==0] = 1
            return data/norms[:,None]
        rings = norm1(rings)
        return [rings]

    decorators = [
                    RingerDecorator( column.format(pidname='tight'  ), basepath + '/ElectronRingerTightTriggerConfig.conf'    , generator ),
                    RingerDecorator( column.format(pidname='medium' ), basepath + '/ElectronRingerMediumTriggerConfig.conf'   , generator ),
                    RingerDecorator( column.format(pidname='loose'  ), basepath + '/ElectronRingerLooseTriggerConfig.conf'    , generator ),
                    RingerDecorator( column.format(pidname='vloose' ), basepath + '/ElectronRingerVeryLooseTriggerConfig.conf', generator ),
                ]
    return decorators



def create_ringer_v8_decorators( column = 'ringer_v8_{pidname}'):

    basepath = os.environ['RINGER_CALIBPATH'] + '/models/Zee/TrigL2_20211114_v8'
    
    def generator( df ):
        columns= ['trig_L2_cl_ring_%d'%i for i in range(100)]
        rings = df[columns].values.astype(np.float32)
        def norm1( data ):
            norms = np.abs( data.sum(axis=1) )
            norms[norms==0] = 1
            return data/norms[:,None]
        rings = norm1(rings)
        return [rings]

    decorators = [
                    RingerDecorator( column.format(pidname='tight'  ), basepath + '/ElectronRingerTightTriggerConfig.conf'    , generator ),
                    RingerDecorator( column.format(pidname='medium' ), basepath + '/ElectronRingerMediumTriggerConfig.conf'   , generator ),
                    RingerDecorator( column.format(pidname='loose'  ), basepath + '/ElectronRingerLooseTriggerConfig.conf'    , generator ),
                    RingerDecorator( column.format(pidname='vloose' ), basepath + '/ElectronRingerVeryLooseTriggerConfig.conf', generator ),
                ]
    return decorators



def create_ringer_v9_decorators( column = 'ringer_v9_{pidname}'):


    basepath = os.environ['RINGER_CALIBPATH'] + '/models/Zee/TrigL2_20211114_v9'

    def generator( df ):
        columns= ['trig_L2_cl_ring_%d'%i for i in range(100)]
        rings = df[columns].values.astype(np.float32)
        def norm1( data ):
            norms = np.abs( data.sum(axis=1) )
            norms[norms==0] = 1
            return data/norms[:,None]

        rings = norm1(rings)
        reta = df['trig_L2_cl_reta'].values.astype(np.float32) / 1.0
        eratio = df['trig_L2_cl_eratio'].values.astype(np.float) / 1.0
        f1 = df['trig_L2_cl_f1'].values.astype(np.float) / 0.6
        f3 = df['trig_L2_cl_f3'].values.astype(np.float) / 0.04
        weta2 = df['trig_L2_cl_weta2'].values.astype(np.float) / 0.02
        wstot = df['trig_L2_cl_wstot'].values.astype(np.float) / 1.0
        eratio[eratio>10.0]=0.0
        eratio[eratio>1.]=1.0
        wstot[wstot<-99]=0
        f1 = f1.reshape((-1,1))
        f3 = f3.reshape((-1,1))
        reta = reta.reshape((-1,1))
        eratio = eratio.reshape((-1,1))
        weta2 = weta2.reshape((-1,1))
        wstot = wstot.reshape((-1,1))
        showers = np.concatenate( (reta,eratio,f1,f3,weta2,wstot), axis=1)  
        return [rings, showers]

    decorators = [
                    RingerDecorator( column.format(pidname='tight'  ), basepath + '/ElectronRingerTightTriggerConfig.conf'    , generator ),
                    RingerDecorator( column.format(pidname='medium' ), basepath + '/ElectronRingerMediumTriggerConfig.conf'   , generator ),
                    RingerDecorator( column.format(pidname='loose'  ), basepath + '/ElectronRingerLooseTriggerConfig.conf'    , generator ),
                    RingerDecorator( column.format(pidname='vloose' ), basepath + '/ElectronRingerVeryLooseTriggerConfig.conf', generator ),
                ]
    return decorators

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
                  verbose=False):

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
        self.__tuning, _ = load_ringer_models(self.path)


    #
    # Decorate the pandas dataframe with output and decision and store into self.column
    #
    def apply(self, df, batch_size=1024):

        df[self.column+'_output'] = np.nan
        df[self.column] = np.nan

        et_bins = self.__tuning['model_etBins']
        eta_bins = self.__tuning['model_etaBins']
   
        # Get L2 values
        et = df[self.et_column].values / GeV
        eta = abs(df[self.eta_column].values)

        # Get the et/eta bin
        etBinIdx = np.digitize( et, et_bins, right=False) - 1
        etaBinIdx = np.digitize( eta, eta_bins, right=False) - 1

        df['etBinIdx'] = etBinIdx
        df['etaBinIdx'] = etaBinIdx

        # Propagate the input and append the output into the dataframe
        for et_bin in df['etBinIdx'].unique():
            for eta_bin in df['etaBinIdx'].unique():
                df_temp = df.loc[ (df['etBinIdx'] == et_bin) & (df['etaBinIdx'] == eta_bin) ]
                if df_temp.shape[0] > 0:
                    MSG_DEBUG(self, 'Propagate for bin (%d, %d)', et_bin, eta_bin) 
                    model = self.__tuning['models'][et_bin][eta_bin]
                    output = model.predict(self.generator(df_temp), verbose=self.verbose, batch_size=self.batch_size)
                    df.at[df_temp.index, self.column+'_output'] = output

        if df[self.column+'_output'].isnull().sum():
            MSG_WARNING(self, 'There is nan values into the %s_output column. Please check!', self.column)

        #
        # Now lets take the decision using the output
        #
        et_bins = self.__tuning['threshold_etBins']
        eta_bins = self.__tuning['threshold_etaBins']
        # Get the et/eta bin
        etBinIdx = np.digitize( et, et_bins, right=False) - 1
        etaBinIdx = np.digitize( eta, eta_bins, right=False) - 1

        df['etBinIdx'] = etBinIdx
        df['etaBinIdx'] = etaBinIdx

        # Take the decision
        for et_bin in df['etBinIdx'].unique():
            for eta_bin in df['etaBinIdx'].unique():
                df_temp = df.loc[ (df['etBinIdx'] == et_bin) & (df['etaBinIdx'] == eta_bin) ]
                if df_temp.shape[0] > 0:
                    MSG_DEBUG(self, 'Decide for bin (%d, %d)', et_bin, eta_bin) 
                    c = self.__tuning['thresholds'][et_bin][eta_bin]
                    output = df_temp[self.column+'_output'].values 
                    thresholds = (df_temp['avgmu'].values * c['slope'] + c['offset'])
                    df.at[df_temp.index, self.column] = np.greater( output, thresholds )
        #df.drop('etBinIdx')

        if df[self.column].isnull().sum():
            MSG_WARNING(self, 'There is nan values into the %s_output column. Please check!', self.column)

        # drop temp columns
        df.drop(['etBinIdx', 'etaBinIdx'], axis=1, inplace=True)
