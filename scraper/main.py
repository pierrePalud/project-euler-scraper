import os
import time

import scrap_fct as scr
import user_prog_fct as user
import plot_prog_fct as prog
import constants as c


if __name__ == '__main__':
    print(f"Importation of Project Euler problems data Started on {time.ctime()}.")
    df_euler = scr.scrape_euler_problems_global()
    print("Importation of Project Euler problems data Successful.")

    df_euler = user.add_user_progression(df_euler)

    df_euler.to_csv(os.path.join(c.RESULT_DIR, 'project-euler-problems.csv'))
    prog.plot_progression(df_euler)

    print(f"Importation of Data from Project Euler Successfull. Results saved in './{c.RESULT_DIR}'.")