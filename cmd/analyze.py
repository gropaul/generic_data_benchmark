import pandas as pd
import plotly.express as px

from src.analyze.load_data import load
from src.analyze.process_data import process_data


def plot_parallel_coordinates(df: pd.DataFrame):
    # Create a mapping from strings to numerical codes
    categorical_mappings = {}
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = df[column].astype('category')
        categorical_mappings[column] = dict(enumerate(df[column].cat.categories))
        df[column] = df[column].cat.codes

    dimensions = df.columns

    min_runtime = df['runtime'].min()
    max_runtime = df['runtime'].max()
    print(f'Min runtime: {min_runtime}')
    print(f'Max runtime: {max_runtime}')

    # Generate the parallel coordinates plot
    fig = px.parallel_coordinates(df, color="runtime",
                                  dimensions=dimensions,
                                  color_continuous_scale=px.colors.diverging.Tealrose,
                                  color_continuous_midpoint=(min_runtime + max_runtime) / 2)

    # Update the tickvals and ticktext for categorical dimensions
    for dim in fig.data[0].dimensions:
        if dim['label'] in categorical_mappings:
            dim['tickvals'] = list(categorical_mappings[dim['label']].keys())
            dim['ticktext'] = list(categorical_mappings[dim['label']].values())

    fig.show()


def plot_runtime_over_duplicates_per_version(df: pd.DataFrame):
    # Generate the scatter plot
    fig = px.scatter(df, x='duplicates', y='runtime', color='version_name', log_x=True, trendline='ols')
    fig.show()


if __name__ == '__main__':
    data = load('cyclic_join')
    data = process_data(data)

    # plot_runtime_over_duplicates_per_version(data)
    # plot_parallel_coordinates(data)