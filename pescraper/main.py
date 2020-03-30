import os
import time

import pescraper.scrap_fct as scr
import pescraper.user_prog_fct as user
import pescraper.plot_prog_fct as prog
import pescraper.constants as c


if __name__ == '__main__':
    for dir_name in [c.DATA_DIR, c.RESULT_DIR]:
        if not(os.path.isdir(dir_name)):
            os.mkdir(dir_name)
        
    print(f"Importation of Project Euler problems data Started on {time.ctime()}.")
    df_euler = scr.scrape_euler_problems_global()
    print("Importation of Project Euler problems data Successful.")

    df_euler = user.add_user_progression(df_euler)

    df_euler.to_csv(os.path.join(c.RESULT_DIR, 'project-euler-problems.csv'))
    
    if 'Solved On' in df_euler.columns:
        prog.plot_progression(df_euler)

    print(f"Importation of Data from Project Euler Successfull. Results saved in './{c.RESULT_DIR}'.")