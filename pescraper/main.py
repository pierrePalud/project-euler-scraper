import os
import time

import pescraper.scrap_fct as scr
import pescraper.user_prog_fct as user
import pescraper.plot_prog_fct as prog
import pescraper.constants as c


if __name__ == '__main__':
    # check existence of data and result directories, and create them emtpy if necessary
    for dir_name in [c.DATA_DIR, c.RESULT_DIR]:
        if not(os.path.isdir(dir_name)):
            os.mkdir(dir_name)
    
    # step 1 - scrape project euler problems data
    print(f"Importation of Project Euler problems data Started on {time.ctime()}.")
    df_euler = scr.scrape_euler_problems_global()
    print("Importation of Project Euler problems data Successful.")

    # step 2 - get user data
    df_euler = user.add_user_progression(df_euler)

    # step 3 - solve result table
    df_euler.to_csv(os.path.join(c.RESULT_DIR, 'project-euler-problems.csv'))
    
    # step 4 - plot and save user progression
    if 'Solved On' in df_euler.columns:
        df_solved = prog.filter_dataframe(df_euler)
        prog.plot_progression(df_solved)

    print(f"Importation of Data from Project Euler Successfull. Results saved in './{c.RESULT_DIR}'.")