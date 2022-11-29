import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime, timedelta

OUTPUT_NAME = 'covid-simulation.png'

def dates_iterate(start_date: str, end_date: str) -> datetime:
    """
    Determines the next simulation date in the range from start to end

    Arguments:
        - start_date: start date of this COVID-19 spread study
        - end_date: end date of this COVID-19 spread study

    Returns:
        - next simulation date
    """
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    for date_offset in range(int((end_date - start_date).days) + 1):
        yield (start_date + timedelta(date_offset)).strftime("%Y-%m-%d")

        
def get_filepath(filename):
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    filepath = os.path.join(source_dir, filename)
    return filepath


def save_plot(fig, filename):
    filepath = get_filepath(filename)    
    fig.savefig(filepath, dpi=300)


def read_dataset(filename):
    filepath = get_filepath(filename)
    df = pd.read_csv(filepath, sep=',', header= 0)
    return df


def create_plot(summary_csv, countries):

    states_timeseries_df = read_dataset(summary_csv)
    print(f'Plotting is being prepared for the following dataset ...')
    print(states_timeseries_df)

    states_timeseries_df = states_timeseries_df[['country', 'date', 'H', 'I', 'S', 'M', 'D']]
    states_timeseries_df['date'] = pd.to_datetime(states_timeseries_df['date'])
    states_timeseries_df.set_index('date')

    countries_num = len(countries)
    fig, ax = plt.subplots(countries_num, figsize =(16, 9*countries_num))

    for i in range(countries_num):
        states_timeseries_df[states_timeseries_df['country'] == countries[i]].plot(
            kind= 'bar', 
            x= 'date', 
            stacked=True, 
            width = 1, 
            color=['green', 'darkorange', 'indianred', 'lightseagreen', 'slategray'],
            ax = ax[i]
        )

        ax[i].legend(['Healthy', 'Infected (without symptoms)', 'Infected (with symptoms)', 'Immune', 'Deceased'])
        ax[i].set_xticklabels(ax[i].get_xticks(), rotation = 30)

        plot_name = countries[i]
        ax[i].set_title(f"Covid Infection Status in {plot_name}")
        ax[i].set_xlabel("Date")
        ax[i].set_ylabel("Population in Millions")

        ax[i].xaxis.set_major_locator(md.MonthLocator())
        selected_dates = states_timeseries_df['date'].dt.to_period('M').unique()
        ax[i].set_xticklabels(selected_dates.strftime('%b %Y'), rotation=30, horizontalalignment= "center")

    save_plot(fig, f'{OUTPUT_NAME}')
    print(f'Plotting Done!')
