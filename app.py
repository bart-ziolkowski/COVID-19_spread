from typing import List, Tuple
from datetime import datetime
from csv import DictReader, DictWriter
from numpy.random import choice
from help_funcs import get_filepath, create_plot, dates_iterate
from sim_parameters import TRASITION_PROBS, HOLDING_TIMES


class StatesCounter:
    '''
    Class for keeping track of the current number of occurrences for each health state

    Attributes:
        - states_occurances: a dictionary containing a summary of the current number of occurrences for each health state
    '''
    def __init__(self, states_occurances: dict = None):
        if states_occurances is None:
            states_occurances = {}

        self.states_occurances_ = states_occurances

        for state in list(HOLDING_TIMES.values())[0].keys():
            self.states_occurances_[state] = 0
    
    def increment_state_occurance(self, state: str) -> None:
        """
        Increments the number of occurrences of the input state

        Arguments:
            - state: name of the health state
        
        Returns:
            - None
        """
        self.states_occurances_[state] += 1


def create_sample_populations(countries: List[str], sample_ratio: float,
                                age_groups: List[str], input_dataset: List[dict]) -> List[dict]:
    """
    Step 2:
        - Create a sample population for each country considering its population and age group distribution

    Arguments:
        - countries: countries for which the simulation is carried out
        - sample_ratio: sampling ratio
        - age_groups: names of all age groups
        - input_dataset: population and age group distribution data of all countries

    Returns:
        - population samples for the simulated countries
    """
    print('Sample populations are being generated ...')

    all_countries_samples = []
    country_sample_amount = 0

    for country in countries:
        country_sample = {}
        country_sample['country'] = country
        country_info = [country_row for country_row in input_dataset
                            if country_row['country'] == country][0]
        country_sample_amount = int(float(country_info.get('population')) / sample_ratio)

        for age_group in age_groups:
            country_sample[age_group] = int(country_sample_amount * float(country_info.get(age_group)) / 100)

        all_countries_samples.append(country_sample)

    return all_countries_samples


def create_timeline_for_individuals(all_countries_samples: List[dict], age_groups: List[str], simulation_dates: List[datetime]) -> Tuple[List[dict], int]:
    """
    Step 3:
        - Create a timeline for each individual from each population sample of every simulated country

    Arguments:
        - all_countries_samples: data on the number of samples for each age group of every simulated country
        - age_groups: names of all age groups
        - simulation_dates: all dates from the beginning to the end of the observation of the spread of COVID-19

    Returns:
        - timelines for all individuals, including information (to be filled in) on previous and current health status in relation to each simulation day (long table), ID of last individual

    """
    print('Timeline for each individual is being generated ...')

    people_ids = 0
    dataset_to_markov = []  

    for population in all_countries_samples:
        for age_group in age_groups:
            for individual_in_age_group in range(int(population.get(age_group))):
                for date in simulation_dates:
                    individual_info = {}
                    individual_info['person_id'] = people_ids
                    individual_info['age_group_name'] = age_group
                    individual_info['country'] = population.get('country')
                    individual_info['date'] = date
                    individual_info['state'] = 'H'
                    individual_info['staying_days'] = 0
                    individual_info['prev_state'] = 'H'
                    dataset_to_markov.append(individual_info)

                people_ids += 1
    
    return dataset_to_markov, people_ids


def apply_markov_chain_for_individuals(people_ids: int, dataset_to_markov: List[dict]) -> None:
    """
    Step 4:
        1) Run the Markov Chain for each individual within period of simulation time and therefore fill in the timeline long table

        2) Save it in covid-simulated-timeseries.csv

    Arguments:
        - people_ids: ID of last individual (to quickly determine the scope of the timeline for-loop)
        - dataset_to_markov: timelines for all individuals

    Returns:
        - None
    """
    print('The Markov for each individual is being applied ...')

    for individual_id in range(people_ids):
        individual_timeline = list(filter(lambda timelines: timelines.get('person_id') == individual_id, dataset_to_markov))
        individual_age_group_name = individual_timeline[0].get('age_group_name')
        days_left_to_next_state = HOLDING_TIMES.get(individual_age_group_name).get(individual_timeline[0].get('state'))

        for day_nr, day_in_timeline in enumerate(individual_timeline[1:], start = 1):
            day_in_timeline['prev_state'] = individual_timeline[day_nr - 1].get('state')

            if days_left_to_next_state == 0:
                probs_values = TRASITION_PROBS.get(individual_age_group_name).get(day_in_timeline.get('prev_state'))
                day_in_timeline['state'] = choice(list(probs_values.keys()), p = list(probs_values.values())) 
                days_left_to_next_state = HOLDING_TIMES.get(individual_age_group_name).get(day_in_timeline.get('state'))
            else:
                days_left_to_next_state -= 1
                day_in_timeline['staying_days'] = individual_timeline[day_nr - 1].get('staying_days') + 1
                day_in_timeline['state'] = individual_timeline[day_nr - 1].get('state')

    print('File covid-simulated-timeseries.csv is being generated ...')

    with open(get_filepath('covid-simulated-timeseries.csv'), 'w', newline='') as created_file:
        column_names = list(dataset_to_markov[0].keys())
        file_writer = DictWriter(created_file, fieldnames=column_names)
        file_writer.writeheader()
        file_writer.writerows(dataset_to_markov)


def accumulate_states_for_countries(dataset_to_markov: List[dict], all_states: List[str]) -> None:
    """
    Step 5:
        1) Summarize the number of states for each date for each simulated country

        2) Save it in covid-summary-timeseries.csv

    Arguments:
        - dataset_to_markov: timelines for all individuals, including information on previous and current health status in relation to each simulation day (long table)
        - all_states: symbols for all states of health

    Returns:
        - None
    """
    print('The number of each health state is being accumulated ...')

    with open(get_filepath('covid-summary-timeseries.csv'), 'w', newline='') as created_file:
        column_names = list(dataset_to_markov[0].keys())[2:4] + all_states
        file_writer = DictWriter(created_file, fieldnames=column_names)
        file_writer.writeheader()

        accumulated_dicts = {}
        for element_in_markov_data in dataset_to_markov:
            country_date_key = (element_in_markov_data["country"], element_in_markov_data["date"])

            if country_date_key not in accumulated_dicts:
                accumulated_dicts[country_date_key] = StatesCounter()
            
            accumulated_dicts[country_date_key].increment_state_occurance(element_in_markov_data["state"])
        
        for country_date_names, states_counter in accumulated_dicts.items():
            country, date = country_date_names
            accumulated_dict = {'country': country, 'date': date}
            accumulated_dict.update(states_counter.states_occurances_)
            file_writer.writerow(accumulated_dict)

    print('File covid-summary-timeseries.csv has been created ...')


def run(countries_csv_name: str, countries: List[str], sample_ratio: float, start_date: str, end_date: str) -> None:
    """
    Plot a charts of the spread of COVID-19 for given countries

    Arguments:
        - countries_csv_name: a name of the .CSV file with the population and age group distribution data of all countries
        - countries: countries for which charts will be plotted
        - sample_ratio: sampling ratio
        - start_date: start date of this COVID-19 spread study
        - end_date: end date of this COVID-19 spread study

    Returns:
        - None 
    """
    print('File', countries_csv_name, 'is being processed ...')

    # Read 'countries_csv_name' file and store it in list of dictionaries
    with open(get_filepath(countries_csv_name)) as opened_file:
        input_dataset = [dict(country_info) for country_info in DictReader(opened_file)]
    
    age_groups = list(input_dataset[0].keys())[3:]
    simulation_dates = list(dates_iterate(start_date, end_date))
    all_states = list(list(HOLDING_TIMES.values())[0].keys())

    all_countries_samples = create_sample_populations(countries, sample_ratio, age_groups, input_dataset)
    
    dataset_to_markov, people_ids = create_timeline_for_individuals(all_countries_samples, age_groups, simulation_dates)

    apply_markov_chain_for_individuals(people_ids, dataset_to_markov)
    
    accumulate_states_for_countries(dataset_to_markov, all_states)

    # Plot the charts
    create_plot(get_filepath('covid-summary-timeseries.csv'), countries)
