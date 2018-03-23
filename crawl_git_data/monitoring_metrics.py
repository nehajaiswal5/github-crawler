__author__ = 'nkumari'
import sys
import requests
import json
import pandas as pd
import numpy as np
import cPickle
import sys
import os
import check_if_exists as checks
import unittest

filename='data.csv'

if os.path.exists(filename):
    df=pd.read_csv(filename)


def read_data(filename):
    '''
     read data file and generate basic dataframes.
     @input filename : str
     @return : df
    '''
    if os.path.exists(filename):
        df=pd.read_csv(filename)

    return df

def get_sorted_list_all_contributors(df):
    '''
        Generate a file to store the count of all repos
    '''
    repo_results = df.groupby(['repo']).size().reset_index(name='repo_count')
    sorted_repo_results=repo_results.sort_values(by='repo_count', ascending=False)

    sorted_repo_results.to_csv('repositories_count.csv')


def get_top_n(n, df):
    '''
        get top n repos across all contributors
        @input n: input top list
        @return df_top_n: dataframe reflecting top n
    '''
    repo_results = df.groupby(['repo']).size().reset_index(name='repo_count')
    sorted_repo_results=repo_results.sort_values(by='repo_count', ascending=False)

    df_top_n=sorted_repo_results[:n]
    return df_top_n


def main():
    read_data('data.csv')

if __name__ == "__main__":
    try:
        main()
    except Exception:
        raise


class UnitTests(unittest.TestCase):

    def test_no_of_parent_user(self):
        self.assertEqual(len(set(df['parent_org'])),3)

    def test_no_of_parent_repo(self):
        self.assertEqual(len(set(df['parent_repo'])),3)

    def test_get_top_n(self):
        self.assertEqual(len(get_top_n(5,df)['repo']),5)

    def test_get_top_n_data(self):
        expected_records=['kubernetes','kubernetes.github.io','test-infra','contrib','docker']
        records=get_top_n(5,df)['repo'].values
        for rec,exp_rec in zip(records,expected_records):
            self.assertEqual(rec,exp_rec)



if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

