


__all__ = ['load_in_loop', 'load_hdf', 'save_hdf']

from Gaugi import progressbar
import pandas as pd


def save_hdf( df , oname):
    df.to_hdf(oname, key='df', mode='w')

def load_hdf( iname ):
    return pd.read_hdf(iname)


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
    