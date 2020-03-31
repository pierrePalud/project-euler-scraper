import os
import pandas as pd
from datetime import datetime


class UserProgressionIntegrator:
    
    def __init__(self, input_dir='input'):
        self.input_dir = input_dir
        self.last_record_filename = self.getLastRecordFilename()
        
        if self.last_record_filename is not None:
            self.buildUserProgressTable()


    def getLastRecordFilename(self):
        list_hist_files = [f for f in os.listdir(self.input_dir) if os.path.isfile(os.path.join(self.input_dir, f))]

        if len(list_hist_files) > 0:
            list_hist_dates = [fname.split('_history_')[1][:-4] for fname in list_hist_files]
            list_hist_dates = [datetime.strptime(date_, '%Y_%m_%d_%H%M') for date_ in list_hist_dates]

            idx_max = list_hist_dates.index(max(list_hist_dates))
            last_record_filename = list_hist_files[idx_max]
            return last_record_filename

        else:
            return None


    def buildUserProgressTable(self):
        list_solved = []
        with open(os.path.join(self.input_dir, self.last_record_filename)) as file:
            file_raw = file.read().split("\n")
            for row in file_raw:
                if row != '':
                    dict_ = {'number':int(row.split(': ')[0]), 'Solved On':row.split(': ')[1]}
                    list_solved.append(dict_)

        df_solved = pd.DataFrame(list_solved)
        df_solved = df_solved.set_index('number')
        df_solved['Solved On'] = pd.to_datetime(df_solved['Solved On'], format='%d %b %y (%H:%M)')
        self.df_solved = df_solved



    def addUserProgression(self, df_euler):
        if self.last_record_filename is not None:
            df_euler = pd.merge(df_euler, self.df_solved, left_index=True, right_index=True, how='outer')
            df_euler['Solved'] = (~pd.isnull(df_euler['Solved On']))
        
            print("User Progression data added to table.")
            return df_euler

        else:
            print(f"No File found in './{self.input_dir}', user progression could not be added.")
            print("Please add a Project Euler history txt file in this directory.")
            print("To download this txt file, please go to https://projecteuler.net/history\n")
            return df_euler