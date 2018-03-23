__author__ = 'nkumari'
from github import Github
import pandas as pd
import numpy as np
import cPickle
import sys
import os
import check_if_exists as checks
import monitoring_metrics as mm

MAXCHARS = slice(0,5000)
### reference: https://help.github.com/articles/authorizing-a-personal-access-token-for-use-with-a-saml-single-sign-on-organization/
GIT_TOKEN='<Put the github token here.>'
FILENAME='data.csv'

def encode_str(s):
    """
    Converts s to unicode.
    :param s: obj to be converted
    :param _limit: Max length of output string
    :return: Output string where new lines are escaped
    """
    _limit=MAXCHARS
    result = unicode(s).encode("utf-8")[_limit]
    return result.replace("\n", '')


## used the git token I generated from my personal account.(because getting throttled all the time)
## reference: https://help.github.com/articles/authorizing-a-personal-access-token-for-use-with-a-saml-single-sign-on-organization/
g = Github(GIT_TOKEN)
#g = Github("<git userid>", "<git password>")


# Pickle Functions to read-write object
# Used in order to serialize object and store locally.
def load_pickle(filename):
    f = open(filename,"rb")
    p = cPickle.load(f)
    f.close()
    return (p)

def make_pickle(filename, data_obj):
    f = open(filename,"wb")
    cPickle.dump(data_obj, f)
    f.close()


# Ignore this section because of throttling
#def read_git_using_api(parent_user,parent_repo):
    # for i in range(1, 100):
    #     r = requests.get("https://api.github.com/repos/"+parent_user+"/"+parent_repo+"/"+"contributors?page="+str(i))
    #     if (r.content is None or len(r.content) == 0 ):
    #         break;
    #     else:
    #         json_data=r.content
    #         for data in json.loads(json_data):
    #             print data
    #             contributors = data['login']
    #             r1=requests.get("https://api.github.com/users/"+contributors+"/repos?page="+str(i))
    #             if (r1.content is None or len(r1.content) == 0 ):
    #                 break;
    #             else:
    #                 json_data1=r1.content
    #                 for d in json.loads(json_data1):
    #                     repo=d['name']
    #                     print contributors, repo


def read_existing_data(fname):
    '''
    Read the existing dataframe
    if there is no file, then create it.

    @input fname: name of the file
    @return df
    '''
    try:
        if os.path.exists(fname):
            if os.stat(fname).st_size != 0:
                df=pd.read_csv(fname)
                if df is not None:
                    return df
                else:
                    return df
        else:
            open(FILENAME,'a')
    except Exception, e:
        open(FILENAME,'a')
        sys.stderr.write("Something happend while reading the datafile, created a new one!")


def create_dataset_next(git_df, parent_org, parent_repo):
    '''
    Creates a new data.csv file in case there is no data available. Otherwise, appends the newly founded data.
    It checks for whether or not entity already exists and then accordingly it adds the parent or children.

    @input: git_df : existing dataframe
    @input: parent_org: parent org/user
    @input: parent_repo: parent repo
    '''
    try:
        #  datafile exists but it's empty
        if os.path.exists(FILENAME) and os.stat(FILENAME).st_size == 0:
            #open the file in write mode
            fp=open(FILENAME,'w')
            # add the header to the csv since it's the first attempt to write to the file
            header=encode_str("parent_org")+','+encode_str("parent_repo")+','+encode_str("contributor")+','+encode_str("repo")+'\n'
            fp.write(header)
            # get the parent user using github api
            org1=g.get_user(parent_org)
            # get all repository of the parent user using github api
            repos1 = org1.get_repo(parent_repo)
            cnt=1
            for r in repos1.get_contributors():
                for repo in r.get_repos():
                    #write the data in a csv
                    result=encode_str(parent_org)+','+encode_str(parent_repo)+','+encode_str(r.login)+','+encode_str(repo.name)+'\n'
                    fp.write(result)
                # maintain a counter of contributors for troubleshooting purposes
                print "Fetched contributor=%d" % cnt +" for given org and repo combo."
                cnt+=1
            # close the file
            fp.close()

        # datafile exists and file is not empty
        if os.stat(FILENAME).st_size != 0:
            #open the file in append mode
            fp=open(FILENAME,'a')
            try:
                # get the parent user using github api
                org1=g.get_user(parent_org)
                # get all repository of the parent user using github api
                repos1 = org1.get_repo(parent_repo)
                cnt=1
                for contributor in repos1.get_contributors():
                    # check if contributor already exists
                    if (checks.check_contributor_existed(git_df,contributor.login) != True):
                        for repo in contributor.get_repos():
                             # check if repo already exists for this contributor
                            if checks.check_repo_existed(git_df,repo.name) != True:

                                result=encode_str(parent_org)+','+encode_str(parent_repo)+','+encode_str(contributor.login)\
                                       +','+encode_str(repo.name)+'\n'
                                # find and append the newly founded records to the file.
                                fp.write(result)
                            else:
                                print "Repo already exists for this contributor!"
                    else:
                        print "Contributor already exists!"

                    # maintain a counter of contributors for troubleshooting purposes
                    print "Fetched contributor=%d" % cnt +" for given org and repo combo."
                    cnt+=1

                fp.close()


            except Exception, e:
                sys.stderr.write("Org/user not found!",e)
                exit(1)
                raise

    except Exception, e:
        sys.stderr.write("Some error occured while processing!",e)
        raise


def main():

    try:
        path=raw_input("Enter the path for the target github repository:")
        if path != "":
            # split the path to get parent user and repo
            paths=path.split('/')
            org=paths[0]
            org_repo=paths[1]
            git_df=read_existing_data(FILENAME)
            # if org/user and repo data already exists then no need to add those.
            if not (checks.check_parent_org_existed(git_df,org) & checks.check_parent_repo_existed(git_df,org_repo)):
                print "Fetching GitHub data for org: %s" % org + " and repo: %s" % org_repo
                # call the create dataset function
                create_dataset_next(git_df, org, org_repo)
                print "Fetching Complete."
            else:
                print "This org, user and repo data already exists!!"
            #reload the dataframe
            updated_git_df=mm.read_data(FILENAME)
            print "Generate all count!!"
            # check the file generated named: repositories_count.csv
            mm.get_sorted_list_all_contributors(updated_git_df)

            # show the top 10 results
            print "Here is the top 10!!"
            top_10_repos= mm.get_top_n(10,updated_git_df)
            for rec in top_10_repos.iterrows():
                print "Repo: %s" % rec[1]['repo'] +" and it's count= %s" % rec[1]['repo_count']

        else:
            sys.stderr.write("Please enter valid path!")

    except Exception, e:
        sys.stderr.write("Some error reading and processing data from github!")
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception:
        raise