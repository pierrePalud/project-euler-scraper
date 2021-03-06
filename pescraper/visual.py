import os

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import constants as c


class ProgressionVisual:
    """Builder of the progression graphs
    
    Attributes
    ----------
    df_solved : pandas.DataFrame
        dataframe with user's solved problems data
    """
    
    def __init__(self, df_euler):
        """Class constructor"""
        self.getSolvedProblemsHistory(df_euler)
        
    
    def getSolvedProblemsHistory(self, df_euler):
        """gets the dataframe of solved problems
        
        Parameters
        ----------
        df_euler : pandas.DataFrame
            full dataframe
        """
        df_solved = df_euler[df_euler['Solved']]
        df_solved = df_solved[['Difficulty rating', 'Solved On', 'Solved']]
        df_solved = df_solved.set_index('Solved On')
        df_solved = df_solved.sort_index()
        self.df_solved = df_solved


    def plotProgression(self, n_days, n_prob):
        '''Plots the user progression and saves the figure in a 
        png file.

        Parameters
        ----------
        n_days : int
            number of days to consider for partial temporal historical

        n_prob : int
            number of problems to consider for partial problems historical            
        '''
        fig, ax = plt.subplots(nrows=3, ncols=4, sharex='col', figsize=(12,8))    

        ## column 1
        ax[0,0].set_title('Total History')
        ax[0,0].step(
            self.df_solved.index, 
            self.df_solved['Solved'].cumsum(), 
            where='post'
        )
        ax[1,0].step(
            self.df_solved.index, 
            self.df_solved['Difficulty rating'].cumsum(), 
            where='post'
        )
        ax[2,0].step(
            self.df_solved.index, 
            self.df_solved['Difficulty rating'].cumsum() / self.df_solved['Solved'].cumsum(),
            where='post'
        )

        # column 2
        df_solved_last_n_days = self.df_solved[self.df_solved.index >= datetime.now() - timedelta(days=n_days)]

        ax[0,1].set_title(f'Last {n_days} days')
        ax[0,1].step(
            df_solved_last_n_days.index, 
            df_solved_last_n_days['Solved'].cumsum(), 
            where='post'
        )
        ax[1,1].step(
            df_solved_last_n_days.index, 
            df_solved_last_n_days['Difficulty rating'].cumsum(), 
            where='post'
        )
        ax[2,1].step(
            df_solved_last_n_days.index, 
            df_solved_last_n_days['Difficulty rating'].cumsum() / df_solved_last_n_days['Solved'].cumsum(),
            where='post'
        )

        # column 3
        ax[0,2].set_title('Total History')
        ax[0,2].step(
            range(1,len(self.df_solved.index)+1), 
            self.df_solved['Difficulty rating'], 
            where='post'
        )
        ax[1,2].step(
            range(1,len(self.df_solved.index)+1), 
            self.df_solved['Difficulty rating'].cumsum(), 
            where='post'
        )
        ax[2,2].step(
            range(1,len(self.df_solved.index)+1), 
            self.df_solved['Difficulty rating'].cumsum() / self.df_solved['Solved'].cumsum(),
            where='post'
        )

        # column 4
        df_solved_last_n_prob = self.df_solved.tail(n_prob)

        ax[0,3].set_title(f'Last {n_prob} Problems')
        ax[0,3].step(
            range(1,len(df_solved_last_n_prob.index)+1), 
            df_solved_last_n_prob['Difficulty rating'], 
            where='post'
        )
        ax[1,3].step(
            range(1,len(df_solved_last_n_prob.index)+1), 
            df_solved_last_n_prob['Difficulty rating'].cumsum(), 
            where='post'
        )
        ax[2,3].step(
            range(1,len(df_solved_last_n_prob.index)+1),
            df_solved_last_n_prob['Difficulty rating'].cumsum() / df_solved_last_n_prob['Solved'].cumsum(),
            where='post'
        )

        # x-axis titles
        for col in range(2):
            plt.sca(ax[2, col])
            plt.xticks(rotation=90)
            ax[2,col].set_xlabel('date')

        for col in range(2,4):
            ax[2,col].set_xlabel('nth solved problem')

        # y-axis titles
        ax[0,0].set_ylabel('# solved problems')
        ax[1,0].set_ylabel('Total difficulty')
        ax[2,0].set_ylabel('Avg difficulty')

        ax[0,2].set_ylabel('Difficulty rating')
        ax[1,2].set_ylabel('Total difficulty')
        ax[2,2].set_ylabel('Avg difficulty')

        # set grids
        for i in range(3):
            for j in range(4):
                ax[i,j].grid()

        fig.tight_layout()
        plt.savefig(os.path.join(c.OUTPUT_DIR, 'project-euler-progression.png'))