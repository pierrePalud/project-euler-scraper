import os
import time

import getopt
import sys

from scraper import ProblemsScraper
from user_progression import UserProgressionIntegrator
from visual import ProgressionVisual

import constants as c


class ProjectEulerScraper:
    """main program class
    
    Attributes
    ----------
    n_days : int (default 60)
        number of days to show in the progress visualization
    
    n_prob : int (default 30)
        number of problems to show in the progress visualization
    """
    
    def __init__(self, argv):  
        """Class constructor. Extracts n_days and n_prob from the command line
        arguments, if they were passed
        
        Parameters
        ----------
        argv : list
            command line arguments passed to script (sys.argv[1:])
        """
        self.n_days = 60
        self.n_prob = 30
        
        arg_struct = 'main.py -d <n_days> -p <n_prob>' 
                
        try:
            opts, args = getopt.getopt(
                argv, "hdp", ["n_days", "n_prob"]
            )
        except getopt.GetoptError:
            print(self.arg_struct)
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print(arg_struct)
                sys.exit()

            elif opt in ("-d", "--n_days"):
                if not(isinstance(arg, int) and (arg >= 1)):
                    raise Exception(f"correct syntax : {arg_struct}\nn_days should be a strictly positive integer. {arg} is not.")
                else:
                    self.n_days = arg

            elif opt in ("-p", "--n_prob"):
                if not(isinstance(arg, int) and (arg >= 1)):
                    raise Exception(f"correct syntax : {arg_struct}\nn_prob should be a strictly positive integer. {arg} is not.")
                else:
                    self.n_prob = arg


    def main(self):
        """main method of program"""
        tps0 = time.time()

        # check existence of data and result directories, and create them emtpy if necessary
        for dir_name in [c.INPUT_DIR, c.OUTPUT_DIR]:
            if not(os.path.isdir(dir_name)):
                os.mkdir(dir_name)

        # step 1 - scrape project euler problems data
        print(f"Importation of Project Euler problems data Started on {time.ctime()}.")
        df_euler = ProblemsScraper().scrapeAllProblems()
        print("Importation of Project Euler problems data Successful.")

        # step 2 - get (and save) user data
        df_euler = UserProgressionIntegrator().addUserProgression(df_euler)

        # step 3 - plot and save user progression
        if 'Solved On' in df_euler.columns:
            ProgressionVisual(df_euler).plotProgression(self.n_days, self.n_prob)

        print(f"Process successfull. Results saved in '{c.OUTPUT_DIR}'")
        print(f"Total duration : {time.time() - tps0:.3f} s")
    
    

# run program
if __name__ == '__main__':
    pe = ProjectEulerScraper(sys.argv[1:])
    pe.main()
