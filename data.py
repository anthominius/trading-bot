from openbb_terminal.sdk import openbb
import pandas as pd

def alternative():
    '''
    Provides programmatic access to the commands from within the OpenBB Terminal
    Uses: openbb.alt
    Assumes: from open_terminal.sdk import openbb
             import panda as pd
    '''

    #OSS
    top_repositories = openbb.alt.oss.top
    search_repositories = openbb.alt.oss.search
    repo_star_history = openbb.alt.oss.history
    startups_ross_index = openbb.alt.oss.ross

    #Covid
    historical_deaths = openbb.alt.covid.global_deaths
    slope = openbb.alt.covid.slopes
    stat =  openbb.alt.covid.stat
    historical_cases = openbb.alt.covid.global_cases
    overview = openbb.alt.covid.ov

    #Print contents of alt sdk
    summary = pd.DataFrame.from_dict(top_repositories(sortby='stars',categories='finance',limit=10))
    print(summary[['full_name','open_issues','stargazers_count']])

if __name__ == '__main__':
    alternative()
