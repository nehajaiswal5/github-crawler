__author__ = 'nkumari'
import sys
import json
import pandas as pd
import numpy as np
import unittest
import os

filename='data.csv'

if os.path.exists(filename):
    df=pd.read_csv(filename)


def check_contributor_existed(df,contributor):
    '''
     Check whether contributor exists or not.
    @input df: dataframe
    @input contributor: contributor name
    @return : boolean
    '''
    try:
        if contributor in set(df['contributor']):
            return True
        else:
            return False
    except Exception, e:
        return False



def check_repo_existed(df,repo):
    '''
     Check whether children repo exists or not.
    @input df: dataframe
    @input repo: repo name
    @return : boolean
    '''
    try:
        if repo in set(df['repo']):
            return True
        else:
            return False
    except Exception, e:
        return False


def check_parent_org_existed(df,parent_org):
    '''
     Check whether parent user/organization exists or not.
    @input df: dataframe
    @input parent_org: parent user/organization name
    @return : boolean
    '''
    try:
        if parent_org in set(df['parent_org']):
            return True
        else:
            return False
    except Exception, e:
        return False


def check_parent_repo_existed(df,parent_repo):
    '''
     Check whether parent repo exists or not.
    @input df: dataframe
    @input parent_repo: parent repo name
    @return : boolean
    '''
    try:
        if parent_repo in set(df['parent_repo']):
            return True
        else:
            return False
    except Exception, e:
        return False



class UnitTests(unittest.TestCase):

    def test_check_contributor_existed(self):
        self.assertEqual(check_contributor_existed(df,'ashcrow'), True)

    def test_check_repo_existed(self):
        self.assertEqual(check_repo_existed(df,'fsutil'), True)

    def test_check_parent_org_existed(self):
        self.assertEqual(check_parent_org_existed(df,'kubernetes1'), False)

    def test_check_parent_org_existed(self):
        self.assertEqual(check_parent_org_existed(df,'kubernetes'), True)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)