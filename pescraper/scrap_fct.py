from bs4 import BeautifulSoup
from urllib import request
from tqdm import tqdm
import re

from concurrent.futures import ThreadPoolExecutor
import pandas as pd

import pescraper.constants as c



def get_max_id_archive_problems():
    '''Returns the maximum id of the project euler achived problems
    
    Parameters
    ----------
    None
    
    Returns
    -------
    max_id : int
        the maximum id of the project euler achived problems
    '''
    soup = BeautifulSoup(request.urlopen(c.URL_ARCHIVE).read().decode(), features="lxml")
    content = soup.find_all('p')[0].text
    max_id = re.findall('\d+', content)[1]
    return int(max_id)


def fetch_archive_problem(num):
    '''Returns a dict with a project euler archive problem data, identified
    by its id
    
    Parameters
    ----------
    num : int
        The id of the problem to consider
    
    Returns
    -------
    dict_problem : dict
        dict with the data of the problem
    '''
    url = c.URL_ROOT.format(num)
    soup = BeautifulSoup(request.urlopen(url).read().decode(), features="lxml")

    # get title
    title = soup.find_all('h2')[0].text

    # get description
    content = soup.find_all('div', {'class': 'problem_content'})[0]
    description = content.text[1:-1]
    
    # initiate output dict        
    dict_problem = {
        'number':num,
        'title':title,
        'description':description,
    } 

    # get additional data
    add_info = soup.find_all('span', {'class': 'info noprint'})[0]
    add_info_list = add_info.text.replace('; ', ';').split(';')

    dict_add_info = {}
    for info in add_info_list:
        info_splitted = info.replace('on ', 'on_').replace('by ', 'by_').replace(': ', '_').split('_')
        if info_splitted[0] == 'Published on':
            info_splitted[1] = info_splitted[1].split(', ')[1]
        [k, v] = info_splitted
        dict_add_info[k] = v

    # format additional data
    try:
        dict_add_info['Solved by'] = int(dict_add_info['Solved by'])
    except:
        dict_add_info['Solved by'] = None
    
    try:
        dict_add_info['Difficulty rating'] = int(dict_add_info['Difficulty rating'].replace('%', ''))
    except:
        dict_add_info['Difficulty rating'] = None

    # add these data to output dict
    for k, v in dict_add_info.items():
        dict_problem[k] = v
        
    return dict_problem



def scrape_euler_problems():
    '''Main Project Euler Archive Scraper
    
    Parameters
    ----------
    None
    
    Returns
    -------
    df_euler : pandas.DataFrame
        dataframe with the problems data
    '''
    # step 1 - get the list of problems to scrape
    max_id = get_max_id_archive_problems()
    list_id = list(range(1, max_id + 1))
    
    # step 2 - actually scrape
    list_problems = []
    
    with ThreadPoolExecutor(10) as executer:
        list_df = list(tqdm(executer.map(fetch_archive_problem, list_id), total=len(list_id)))
            
    # step 3 - format the output dataframe
    df_euler = pd.DataFrame(list_df)
    df_euler = df_euler.set_index('number')
    df_euler['Published on'] = pd.to_datetime(df_euler['Published on'])
    
    return df_euler

