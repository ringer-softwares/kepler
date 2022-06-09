


__all__ = ['load_in_loop', 'load_hdf', 'save_hdf', 'load']

from Gaugi import progressbar
import pandas as pd
import numpy as np
import gc

def save_hdf( df , oname):
    df.to_hdf(oname, key='df', mode='w')

def load_hdf( iname ):
    return pd.read_hdf(iname)


#
# Load npz format from kepler dumper and convert to pandas like
#
def load( path ):
    '''
    This function will get a .npz file and transform into a pandas DataFrame. 
    The .npz has three types of data: float, int and bool this function will concatenate these features and reorder them.
    Arguments:
    path (str) - the full path to .npz file
    '''
    # open the file
    d = dict(np.load(path, allow_pickle=True))    
    # create a list of temporary dataframes that should be concateneted into a final one
    df_list = []
    for itype in ['float', 'int', 'bool', 'object']:
        df_list.append(pd.DataFrame(data=d['data_%s' %itype], columns=d['features_%s' %itype]))
    # concat the list
    df = pd.concat(df_list, axis=1)
    # return the DataFrame with ordered features.
    df = df[d['ordered_features']]
    # add the target information
    df['target'] = d['target']
    if 'extra_features' in d.keys():
        aux_df = pd.DataFrame(data=d['extra_data'], columns=d['extra_features'])
        df = pd.concat([df, aux_df], axis=1)
    # remove the list of DataFrame and collect into garbage collector
    del df_list, d
    gc.collect()
    return df



def load_in_loop( paths, drop_columns=[], decorators=[], chains=[]):

    tables = []
        
    for path in progressbar( paths, prefix='Reading files...'):
        df = load_hdf( path )
        for decorator in decorators:
            decorator.apply(df) 
        for column in drop_columns:
            df.drop( column, axis=1, inplace=True )    
        for chain in chains:
            chain.apply(df)
        tables.append(df)

    return pd.concat(tables).reset_index(drop=True)
    