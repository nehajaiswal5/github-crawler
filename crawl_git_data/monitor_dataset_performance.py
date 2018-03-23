__author__ = 'nkumari'

import pandas as pd

def analyze_performance(filename):
    '''
     Check the memory of the file
    '''
    df=pd.read_csv(filename)
    df.info()

analyze_performance('data.csv')


