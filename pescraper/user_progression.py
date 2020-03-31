import os
import pandas as pd
from datetime import datetime


class UserProgressionIntegrator:
    """This class integrates the historical personal data of the user to
    the problems data dataframe
    
    Attributes
    ----------
    last_record_filename : str
        name of the user's most updated historical data file
    """
    
    
    def __init__(self):
        """Class constructor"""
        self.getLastRecordFilename()
        

    def getLastRecordFilename(self):
        """looks for the user's most updated historical data file"""
        list_hist_files = [
            f for f in os.listdir(c.INPUT_DIR) 
            if os.path.isfile(os.path.join(c.INPUT_DIR, f))
        ]

        if len(list_hist_files) > 0:
            list_hist_dates = [fname.split('_history_')[1][:-4] for fname in list_hist_files]
            list_hist_dates = [datetime.strptime(date_, '%Y_%m_%d_%H%M') for date_ in list_hist_dates]

            idx_max = list_hist_dates.index(max(list_hist_dates))
            self.last_record_filename = list_hist_files[idx_max]

        else:
            self.last_record_filename = None


    def buildUserProgressTable(self):
        """Builds the users's progression from the user's most updated 
        historical data file
        
        Parameters
        ----------
        None
        
        Returns
        -------
        df_solved : pandas.DataFrame
            dataframe with id of solved problems and date of solving 
        """
        list_solved = []
        with open(os.path.join(c.INPUT_DIR, self.last_record_filename)) as file:
            file_raw = file.read().split("\n")
            for row in file_raw:
                if row != '':
                    dict_ = {
                        'number':int(row.split(': ')[0]), 
                        'Solved On':row.split(': ')[1]
                    }
                    list_solved.append(dict_)

        df_solved = pd.DataFrame(list_solved)
        df_solved = df_solved.set_index('number')
        df_solved['Solved On'] = pd.to_datetime(df_solved['Solved On'], format='%d %b %y (%H:%M)')
        return df_solved



    def addUserProgression(self, df_euler):
        """merges the df_solved and df_euler dataframes, if the former exists
        
        Parameters
        ----------
        df_euler : pandas.DataFrame
            result of the problems scraping
            
        Returns
        -------
        df_euler : pandas.DataFrame
            possibly improved version of the input
        """
        if self.last_record_filename is not None:
            df_solved = self.buildUserProgressTable()
            df_euler = pd.merge(df_euler, df_solved, left_index=True, right_index=True, how='outer')
            df_euler['Solved'] = (~pd.isnull(df_euler['Solved On']))
        
            print("User Progression data added to table.")
            
        else:
            print(f"No File found in './{c.INPUT_DIR}', user progression could not be added.")
            print("Please add a Project Euler history txt file in this directory.")
            print("To download this txt file, please go to https://projecteuler.net/history\n")
            
        df_euler.to_csv(os.path.join(c.OUTPUT_DIR, 'project-euler-problems.csv'))    
        return df_euler