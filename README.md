# github-crawler

# Problem Definition:

The goal of this challenge is to produce a command-line script that will crawl Github user profiles to produce the following report:

## Milestone 1
Given the full name of a target github repository (e.g. “kubernetes/kubernetes” which refers to https://github.com/kubernetes/kubernetes/),
fetch all of that project’s contributors, and then fetch each contributor’s repositories (i.e. the repos that they have forked).
Count how many times each repository appears across all contributors. Then print to stdout a summary of the top 10 repositories by count.

## Milestone 2
Since this crawl might involve pulling accounts for a large number of users, which could take a long time, or eat up our API rate limit,
we should support saving the contributor / repo data that we need to an on-disk representation,
and using saved data to resume/replay a scan if possible.

# Design Principles:

    The functional design is based on below main aspects:

        1. Only fetch repos not in our database already to save on.
        2. Create a processor in memory for quick queries about the data.
        3. Only compare repository wrt their name.

    The system design should cover:

        1. Scalability
        2. Extensibility
        3. Reliability
        4. Availability


# Assumption/Limitation:

Tried using https://developer.github.com/v3/repos/#list-contributors. however, getting throttled every single time.

Response as below:
403 {u'documentation_url': u'https://developer.github.com/v3/#rate-limiting', u'message': u"API rate limit exceeded for ..my_ip address..
(But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)"}

Hence, used GitHub Python Client - PyGitHub along with my own personal github token, so as to get the data.
I believe for big network it doesn't return full graph of the contributor-repo combination.

Given time, I can explore other ways to expand it, if it doesn't throttle.

I used pandas to do analysis.

# High Level design:

   1. Read the data from github using client PyGithub
   2. Check if user/repo already exist. If they do, then ignore and fetch not existing ones.
   3. Use pandas dataframes to read the dataset in memory that is created as part of step 1&2.
   4. Analyze the data to create monitoring decisions.


# Some system storage considerations:

Storage - k KB to store 1 parent repository data.
          so suppose,
          we have R repositories to process and all are distinct, then in worst case R*k KB will be required.

Time    - C * R times to read and create dataset. where C is # of contributor & R is # of repository


# Algorithm:

-> Very simple crawler: very simple model with 2 loops and by keeping track existing contributor and repo.
   i.e. go to parent repo -> get all contributor -> foreach of these contributor-> get their repos

-> Using graphs: I would like to implement this algorithm using Breadth first Search version for crawling in future as given the time.

# How to use:

  cd ...path../github-crawler/crawl_git_data

  Data Crawler
  ------------
  python data_reader.py
  Enter the path for the target github repository: <Enter the target repository>

  Enter the target repository in this format e.g. - 'kubernetes/kubernetes'  or 'AudioKit/AudioKit'

  GIT_TOKEN=<Git token> replace it with our own personal github token or your own git username and password.
  Follow this link - https://help.github.com/articles/authorizing-a-personal-access-token-for-use-with-a-saml-single-sign-on-organization/

  This will create a file "data.csv" to retain all user/organization contributors and their respestive repositories.

  Data Format
  ------------
  File format of 'data.csv':

    parent_org,parent_repo,contributor,repo

    kubernetes,kubernetes,brendandburns,aci-bridge-k8s
    kubernetes,kubernetes,brendandburns,acs
    kubernetes,kubernetes,brendandburns,acs-build-demos
    kubernetes,kubernetes,brendandburns,acs-engine


    where parent_org,parent_repo is the parent org/user and repo we are starting our crawler with.
          contributor - is the contributor of that parent user
          repo - is the repository of that contributor


  Git Monitoring
  --------------

  python monitoring_metrics.py

  This file contains 2 functionality:
            1. Creates a file which shows repo wise count across all repository available in the dataset.
            2. Returns top 10 repositories with the count.

  Data Analysis.ipynb/Data+Analysis.html  : A Jupyter notebook file with detailed analysis of this dataset.
                                            It contains some additional analysis and methods to run adhoc queries.

  Includes testcases

  Check org/user/repo already exists
  ----------------------------------

   python check_if_exists.py

   This file contains functionalities to check whether user or repo already exist in our system. so that don't we need refetch it or store.
   It keeps track of what we already have in our data.

        : check_contributor_existed, check_repo_existed, check_parent_org_existed, check_parent_repo_existed

   Includes testcases

  Performance Monitoring
  ----------------------

  python  monitor_dataset_performance.py

  This file records the info of data.csv



# Final Result:

    python data_reader.py
    Enter the path for the target github repository:adamnemecek/zipline

    This org, user and repo data already exists!!
    Generate all count!!
    Here is the top 10!!

    Repo: kubernetes and it's count= 379
    Repo: kubernetes.github.io and it's count= 168
    Repo: test-infra and it's count= 155
    Repo: contrib and it's count= 118
    Repo: docker and it's count= 99
    Repo: origin and it's count= 81
    Repo: heapster and it's count= 71
    Repo: cadvisor and it's count= 70
    Repo: features and it's count= 67
    Repo: release and it's count= 65


# References:

https://github.com/PyGithub/PyGithub
http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.contributors_url
https://help.github.com/articles/authorizing-a-personal-access-token-for-use-with-a-saml-single-sign-on-organization/


# Future Extensions:

1. Use hadoop map-reduce or spark job process the data, do basic counts and optimized sort operations.
2. We can also use spark dataframes to do these operations.
3. Dataset can store timestamp wrt date & time of the pull, we can extend the analysis for time-series.
4. If data is saved in a table, we can read the table and do the analysis.
5. This data structure can be extended for storing other metadata too.
6. We can read data in json format too.
7. We can extend this to build a real-time system, where the moment user-repo is fetch, data structure is updated and results too.
8. Use some of the graph databases, to store org/user, contributor, repo network along with their metadatas.
9. Use breadth first search method to navigate the links.

