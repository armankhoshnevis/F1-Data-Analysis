import pandas as pd
import plotly.express as px
import os

def load_pit_stop_data():
    file_path = os.path.join(os.path.dirname(__name__), '.', 'Datasets', 'pit_results.csv')
    df_pit_results = pd.read_csv(file_path)
    return df_pit_results

def load_race_results_data():
    """Loads the race results data from CSV."""
    file_path = os.path.join(os.path.dirname(__name__), '.', 'Datasets', 'race_results.csv')
    df = pd.read_csv(file_path)
    df['constructorId'] = df['constructorId'].replace({'alphatauri': 'rb'})
    discontinued_teams = ['toro_rosso', 'force_india', 'racing_point']
    df = df[~df['constructorId'].isin(discontinued_teams)]
    return df

def plot_avg_pit_stop_duration_by_circuit(year):
    """Plots the average pit stop duration by circuit for a given year."""
    df_pit_results = load_pit_stop_data()
    df_race_results = load_race_results_data()
    file_path = os.path.join(os.path.dirname(__name__), '.', 'Datasets', 'race_schedule.csv')
    race_schedule = pd.read_csv(file_path)
    
    df_race_results_reduced = df_race_results[['season', 'round', 'driverId', 'constructorId']]
    df_pit_results = df_pit_results.merge(df_race_results_reduced, on=['season', 'round', 'driverId'], how='left')
    
    df_pit_results_with_circuits = df_pit_results.merge(
        race_schedule[['season', 'round', 'circuitName']],
        on=['season', 'round'],
        how='left'
    )
    
    df_pit_results_year = df_pit_results_with_circuits[df_pit_results_with_circuits['season'] == year]
    
    avg_pit_stop_duration = df_pit_results_year.groupby('circuitName')['duration'].mean().reset_index()
    
    fig = px.bar(
        avg_pit_stop_duration,
        x='circuitName',
        y='duration',
        labels={'circuitName': 'Circuit', 'duration': 'Avg. Duration (s)'},
        color='duration',
        color_continuous_scale=px.colors.sequential.Viridis,
        hover_data={'duration': ':.2f'}
    )
    
    fig.update_layout(
        xaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    return fig

def plot_pit_stop_duration_by_constructor(year):
    df_pit_results = load_pit_stop_data()
    df_race_results = load_race_results_data()

    df_race_results_reduced = df_race_results[['season', 'round', 'driverId', 'constructorId']]
    df_pit_results = df_pit_results.merge(df_race_results_reduced, on=['season', 'round', 'driverId'], how='left')

    df_pit_results_year = df_pit_results[df_pit_results['season'] == year]

    constructor_mean_durations = df_pit_results_year.groupby('constructorId')['duration'].mean()
    sorted_constructors = constructor_mean_durations.sort_values(ascending=False).index.tolist()

    brand_colors = {
        'mercedes': '#565F64',
        'ferrari': '#ff0000',
        'williams': '#00A0DE',
        'renault': '#FFFF00',
        'haas': '#E6002B',
        'mclaren': '#FF8000',
        'sauber': '#90EE90',
        'alfa': '#000000',
        'alphatauri': '#00008B',
        'alpine': '#C71585',
        'aston_martin': '#006400',
        'red_bull': '#FDD900',
        'rb': '#20394C'
        }
    
    fig = px.box(
        df_pit_results_year,
        x='constructorId',
        y='duration',
        labels={'constructorId': 'Constructor', 'duration': 'Pit Stop Duration (seconds)'},
        category_orders={'constructorId': sorted_constructors},  # Sort x-axis by mean duration
        color='constructorId',
        color_discrete_map=brand_colors,
        hover_data={'duration': ':.2f'}
    )
    
    fig.update_layout(
        xaxis_title='Constructor',
        yaxis_title='Pit Stop Duration (seconds)',
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    return fig

def plot_pit_stop_count_by_lap(year=None, round_num=None):
    """Plots a histogram showing the count of pit stops by lap for a given year and round."""
    df_pit_results = load_pit_stop_data()

    if year:
        df_pit_results = df_pit_results[df_pit_results['season'] == year]
    if round_num:
        df_pit_results = df_pit_results[df_pit_results['round'] == round_num]

    fig = px.histogram(
        df_pit_results,
        x='lap',
        labels={'lap': 'Lap Number', 'count': 'Pit Stop Count'},
        nbins=25
    )

    fig.update_layout(
        xaxis_title='Lap Number',
        yaxis_title='Pit Stop Count',
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        margin=dict(l=50, r=50, t=50, b=50),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    return fig