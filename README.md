# project-euler-scraper

A scraper for Project Euler Problems data and User Progression data. Outputs a table with the collected information and a user progression graph.

# Installation and First Run

```shell
git clone [ssh key of the repo]
cd project-euler-scraper
python setup.py install
python pescraper/main.py
```

# How to include User Progression

By default, user progression is not included. To add it to the output table, please add a Project Euler history txt file in a `./data` directory. To download this txt file, please go to https://projecteuler.net/progress;show=history and click on the link under the table. Then, run `pescraper/main.py` again.



# Note

The algorithm uses multithreading to speed up the download of the problems' data. Depending on your machine, the whole algorithm should take less than a minute to run. 