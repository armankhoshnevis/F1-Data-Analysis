import pandas as pd
import plotly.express as px

def load_lap_times_data():
    """Loads the lap times data from concatenated CSV files."""
    file_paths = [f'./Datasets/lap_times_{year}.csv' for year in range(2017, 2025)]
    dataframes = [pd.read_csv(file) for file in file_paths]
    lap_times_df = pd.concat(dataframes, ignore_index=True)
    return lap_times_df

def convert_time_to_seconds(time_str):
    """Converts lap time from string format 'M:SS.mmm' to seconds."""
    minutes, seconds = time_str.split(':')
    total_seconds = int(minutes) * 60 + float(seconds)
    return total_seconds

def plot_driver_lap_times(year, round_num, lower_percentile=5, upper_percentile=95):
    """Plots a box plot of lap times for all drivers in a given race, filtering out extreme outliers."""
    
    lap_times_df = load_lap_times_data()
    race_schedule_df = pd.read_csv('./Datasets/race_schedule.csv')
    
    race_name = race_schedule_df[(race_schedule_df['season'] == year) & 
                                 (race_schedule_df['round'] == round_num)]['raceName'].values[0]
    
    lap_times_df = lap_times_df[(lap_times_df['season'] == year) & (lap_times_df['round'] == round_num)]
    
    lap_times_df['lap_time_seconds'] = lap_times_df['time'].apply(convert_time_to_seconds)
    
    lower_limit = lap_times_df['lap_time_seconds'].quantile(lower_percentile / 100)
    upper_limit = lap_times_df['lap_time_seconds'].quantile(upper_percentile / 100)
    
    lap_times_filtered = lap_times_df[
        (lap_times_df['lap_time_seconds'] >= lower_limit) &
        (lap_times_df['lap_time_seconds'] <= upper_limit)
    ]
    
    fig = px.box(
        lap_times_filtered,
        x='driverId',
        y='lap_time_seconds',
        title=f'{race_name}',
        labels={'lap_time_seconds': 'Lap Time (seconds)', 'driverId': 'Driver'}
    )
    
    fig.update_layout(
        xaxis_title='Driver',
        yaxis_title='Lap Time (seconds)',
        title_font=dict(size=20),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    
    return fig