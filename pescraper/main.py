import os
import time

import getopt
import sys

from scraper import ProjectEulerScraper
from user_progression import UserProgressionIntegrator
from visual import ProgressionVisual


def get_args(argv):
    args_main = {
        'n_days':60,
        'n_prob':30
    }
    arg_struct = 'main.py -d <n_days> -p <n_prob>' 
    
    try:
        opts, args = getopt.getopt(
            argv, "hdp", ["n_days", "n_prob"]
        )
    except getopt.GetoptError:
        print(arg_struct)
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print(arg_struct)
            sys.exit()
                        
        elif opt in ("-d", "--n_days"):
            if not(isinstance(arg, int) and (arg >= 1)):
                raise Exception(f"correct syntax : {arg_struct}\nn_days should be a strictly positive integer")
            else:
                args_main['n_days'] = arg

        elif opt in ("-p", "--n_prob"):
            if not(isinstance(arg, int) and (arg >= 1)):
                raise Exception(f"correct syntax : {arg_struct}\nn_prob should be a strictly positive integer")
            else:
                args_main['n_prob'] = arg
            
    return args_main


def main(n_days, n_prob):
    tps0 = time.time()
    
    input_dir = 'data'
    output_dir = 'result'
    
    # check existence of data and result directories, and create them emtpy if necessary
    for dir_name in [input_dir, output_dir]:
        if not(os.path.isdir(dir_name)):
            os.mkdir(dir_name)
    
    # step 1 - scrape project euler problems data
    print(f"Importation of Project Euler problems data Started on {time.ctime()}.")
    df_euler = ProjectEulerScraper().scrapeAllProblems()
    print("Importation of Project Euler problems data Successful.")

    # step 2 - get user data
    df_euler = UserProgressionIntegrator(input_dir).addUserProgression(df_euler)

    # step 3 - solve result table
    df_euler.to_csv(os.path.join(output_dir, 'project-euler-problems.csv'))
    
    # step 4 - plot and save user progression
    if 'Solved On' in df_euler.columns:
        ProgressionVisual(df_euler, output_dir).plotProgression(n_days, n_prob)

    print(f"Process successfull. Results saved in './{output_dir}'")
    print(f"Total duration : {time.time() - tps0:.3f} s")
    
    
    
if __name__ == '__main__':
    args = get_args(sys.argv[1:])
    main(**args)