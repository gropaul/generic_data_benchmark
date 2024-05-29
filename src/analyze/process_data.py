import os

import pandas as pd
import matplotlib.pyplot as plt

from src.utils.config import ANALYSIS_RESULTS_DIR


def calculate_speedup(data: pd.DataFrame) -> pd.DataFrame:
    # split the dataset by distinct versions
    versions = data['version_name'].unique()
    columns = data.columns
    baseline = None
    alternatives = []
    for version in versions:
        # get the data for the current version
        version_data = data[data['version_name'] == version]

        # sort by all so that we know that the same query is at the same index
        for column in columns:
            version_data = version_data.sort_values(by=column)

        if version == 'Baseline':
            baseline = version_data
        else:
            alternatives.append(version_data)

    rows = len(alternatives)

    for row in range(rows):
        for df in alternatives:
            alternative_runtime = df['runtime']
            baseline_runtime = baseline['runtime']

            speedup = baseline_runtime / alternative_runtime
            df['speedup'] = speedup
            version_name = df['version_name'].iloc[0]

            df.to_csv(f'{version_name}_speedup.csv', index=False)
    return data


def combine_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    # get all columns that contain 'avg_edges_per_node' in their name
    duplicates_columns = [col for col in data.columns if ('avg_edges_per_node' in col)]

    every_second_column = duplicates_columns[1::2]

    # multiply all columns that contain 'avg_edges_per_node' in their name
    data['duplicates'] = data[every_second_column].product(axis=1)

    # drop all columns that contain 'avg_edges_per_node' in their name
    data = data.drop(columns=duplicates_columns)
    return data


def plot_duration_per_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    # get all rows where the duplicates columns are all the same
    duplicates_columns = [col for col in data.columns if ('avg_edges_per_node' in col)]

    filtered_df = data
    for column in duplicates_columns:
        filtered_df = filtered_df[filtered_df[column] == filtered_df[duplicates_columns[0]]]

    # save the filtered data
    csv_path = os.path.join(ANALYSIS_RESULTS_DIR, 'filtered_duplicates.csv')
    filtered_df.to_csv(csv_path, index=False)

    # plot each version_name
    versions = filtered_df['version_name'].unique()

    version_runtimes = {}
    xs = None

    for version in versions:
        version_data = filtered_df[filtered_df['version_name'] == version]

        # order by duplicates
        version_data = version_data.sort_values(by=duplicates_columns[0])

        ys = version_data['runtime']
        xs = version_data[duplicates_columns[0]]

        version_runtimes[version] = ys

    ys_baseline = version_runtimes['Baseline']

    for version in versions:
        if version == 'Baseline':
            continue

        relative_speedup = []
        for i, runtime in enumerate(version_runtimes[version]):
            speedup = ys_baseline[i] / runtime
            relative_speedup.append(speedup)

        plt.plot(xs, relative_speedup, label=version, marker='x')

    plt.xlabel('Average Chain Length')
    plt.ylabel('Relative Speedup')

    # make both axes logarithmic
    plt.xscale('log')

    # add a legend
    plt.legend()

    # save the plot
    plot_path = os.path.join(ANALYSIS_RESULTS_DIR, 'duplicates_vs_runtime.png')
    plt.savefig(plot_path)
    plt.close()





def process_data(data: pd.DataFrame) -> pd.DataFrame:

    # remove all columns withere there is only one unique value
    data = data.loc[:, data.nunique() > 1]


    # exclude the following columns
    exclude_columns = ['version_github_commit_url']
    data = data.loc[:, ~data.columns.isin(exclude_columns)]
    # calculate_speedup(data)

    plot_duration_per_duplicates(data)

    csv_path = os.path.join(ANALYSIS_RESULTS_DIR, 'cyclic_join.csv')
    data.to_csv(csv_path, index=False)

    data = combine_duplicates(data)

    return data
