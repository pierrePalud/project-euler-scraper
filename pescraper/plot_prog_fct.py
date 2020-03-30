import os

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import pescraper.constants as c


def plot_progression(df_euler, n_days=60, n_prob=30, path_to_output=os.path.join(c.RESULT_DIR, 'project-euler-progression.png')):
    df_solved = df_euler[df_euler['Solved']]
    df_solved = df_solved[['Difficulty rating', 'Solved On', 'Solved']]
    df_solved = df_solved.set_index('Solved On')
    df_solved = df_solved.sort_index()
    
    
    fig, ax = plt.subplots(nrows=3, ncols=4, sharex='col', figsize=(12,8))

    ax[0,0].set_title('Total History')
    ax[0,0].set_ylabel('# solved problems')
    ax[0,0].step(df_solved.index, df_solved['Solved'].cumsum(), where='post')
    ax[0,0].grid()

    ax[1,0].set_ylabel('Total difficulty')
    ax[1,0].step(df_solved.index, df_solved['Difficulty rating'].cumsum(), where='post')
    ax[1,0].grid()

    ax[2,0].set_ylabel('Avg difficulty')
    ax[2,0].step(df_solved.index, 
             df_solved['Difficulty rating'].cumsum() / df_solved['Solved'].cumsum(),
             where='post')
    ax[2,0].grid()

    ax[2,0].set_xlabel('date')


    df_solved_last_n_days = df_solved[df_solved.index >= datetime.now() - timedelta(days=n_days)]

    ax[0,1].set_title(f'Last {n_days} days')
    ax[0,1].step(df_solved_last_n_days.index, df_solved_last_n_days['Solved'].cumsum(), where='post')
    ax[0,1].grid()

    ax[1,1].step(df_solved_last_n_days.index, df_solved_last_n_days['Difficulty rating'].cumsum(), where='post')
    ax[1,1].grid()

    ax[2,1].step(df_solved_last_n_days.index, 
             df_solved_last_n_days['Difficulty rating'].cumsum() / df_solved_last_n_days['Solved'].cumsum(),
             where='post')
    ax[2,1].grid()
    ax[2,1].set_xlabel('date')

    for col in range(2):
        plt.sca(ax[2, col])
        plt.xticks(rotation=90)


    ax[0,2].set_title('Total History')
    ax[0,2].set_ylabel('Difficulty rating')
    ax[0,2].step(range(1,len(df_solved.index)+1), df_solved['Difficulty rating'], where='post')
    ax[0,2].grid()

    ax[1,2].set_ylabel('Total difficulty')
    ax[1,2].step(range(1,len(df_solved.index)+1), df_solved['Difficulty rating'].cumsum(), where='post')
    ax[1,2].grid()

    ax[2,2].set_ylabel('Avg difficulty')
    ax[2,2].step(range(1,len(df_solved.index)+1), 
             df_solved['Difficulty rating'].cumsum() / df_solved['Solved'].cumsum(),
             where='post')
    ax[2,2].grid()

    ax[2,2].set_xlabel('nth solved problem')


    df_solved_last_n_prob = df_solved.tail(n_prob)

    ax[0,3].set_title(f'Last {n_prob} Problems')
    ax[0,3].step(range(1,len(df_solved_last_n_prob.index)+1), df_solved_last_n_prob['Difficulty rating'], where='post')
    ax[0,3].grid()

    ax[1,3].step(range(1,len(df_solved_last_n_prob.index)+1), df_solved_last_n_prob['Difficulty rating'].cumsum(), where='post')
    ax[1,3].grid()

    ax[2,3].step(range(1,len(df_solved_last_n_prob.index)+1), 
             df_solved_last_n_prob['Difficulty rating'].cumsum() / df_solved_last_n_prob['Solved'].cumsum(),
             where='post')
    ax[2,3].grid()

    ax[2,3].set_xlabel('nth solved problem')

    fig.tight_layout()
    plt.savefig(path_to_output)