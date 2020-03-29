from bs4 import BeautifulSoup
from urllib import request
from tqdm import tqdm
import re

from concurrent.futures import ThreadPoolExecutor
import pandas as pd

import constants as c



def get_max_id_archive_problems():
    soup = BeautifulSoup(request.urlopen(c.URL_ARCHIVE).read().decode(), features="lxml")
    
    content = soup.find_all('p')[0].text
    max_id = re.findall('\d+', content)[1]
    return int(max_id)


def fetch_archive_problem(num):
    url = c.URL_ROOT.format(num)

    soup = BeautifulSoup(request.urlopen(url).read().decode(), features="lxml")

    title = soup.find_all('h2')[0].text

    content = soup.find_all('div', {'class': 'problem_content'})[0]
    content_text = content.text
    content_text = content_text[1:-1]

    add_info = soup.find_all('span', {'class': 'info noprint'})[0]
    add_info_list = add_info.text.replace('; ', ';').split(';')

    dict_add_info = {}
    for info in add_info_list:
        info_splitted = info.replace('on ', 'on_').replace('by ', 'by_').replace(': ', '_').split('_')
        if info_splitted[0] == 'Published on':
            info_splitted[1] = info_splitted[1].split(', ')[1]
        [k, v] = info_splitted
        dict_add_info[k] = v

    try:
        dict_add_info['Solved by'] = int(dict_add_info['Solved by'])
    except:
        dict_add_info['Solved by'] = None
    
    try:
        dict_add_info['Difficulty rating'] = int(dict_add_info['Difficulty rating'].replace('%', ''))
    except:
        dict_add_info['Difficulty rating'] = None
        
    dict_problem = {
        'number':num,
        'title':title,
        'description':content_text,
    } 

    for k, v in dict_add_info.items():
        dict_problem[k] = v
        
    return dict_problem


# def scrape_euler_problems(list_id):
#     list_problems = []
#     for i in progressbar.progressbar(range(len(list_id))):
#         num = list_id[i]
#         dict_problem = fetch_archive_problem(num)
#         list_problems.append(dict_problem)
    
#     df_euler = pd.DataFrame(list_problems)
    
#     return df_euler


def scrape_euler_problems(list_id):
    list_problems = []
    
    with ThreadPoolExecutor(10) as executer:
        list_df = list(tqdm(executer.map(fetch_archive_problem, list_id), total=len(list_id)))
            
    df_euler = pd.DataFrame(list_df)
    
    df_euler = df_euler.set_index('number')
    df_euler['Published on'] = pd.to_datetime(df_euler['Published on'])
    
    return df_euler


def scrape_euler_problems_global(min_id=None, max_id=None):
    if min_id is None:
        min_id = 1
    if max_id is None:
        max_id = get_max_id_archive_problems()
    
    list_id = list(range(min_id, max_id + 1))
    
    df_euler = scrape_euler_problems(list_id)
    return df_euler