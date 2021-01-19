#==============================================================================
#title           :grapher.py
#description     :This program graphs reults from covid simulation
#author          :Ricardo Martinez
#date            :October 5th 2020
#python_version  :3.8.6
#email           :mrtzcardo@gmail.com
#github          :github.com/mrtzcardo
#instagram       :@cardo.love
#==============================================================================

from stats_writer import xlsx_stats
import matplotlib.pyplot as plt


def graph_results(health_history, infected_history, dead_history, recover_history, save_results):
    # graph of health data over time
    x = range(0, len(health_history))
    y1 = infected_history
    y2 = health_history
    y3 = recover_history
    y4 = dead_history

    # Basic stacked area chart
    plt.stackplot(x, y1, y2, y3, y4, labels=['Infected', 'Healthy', 'Recovered', 'Dead'])
    plt.legend(loc='upper left')
    plt.show()

    # exports data to .xlsx file
    if save_results:
        xlsx_stats(y1, y2, y3, y4)
