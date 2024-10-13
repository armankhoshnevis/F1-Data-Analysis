import plotly.express as px
import pandas as pd
import os

def load_race_results_data():
    """Loads the race results data from CSV."""
    file_path = os.path.join(os.path.dirname(__name__), '.', 'Datasets', 'race_results.csv')
    df = pd.read_csv(file_path)
    df['constructorId'] = df['constructorId'].replace({'alphatauri': 'rb'})
    discontinued_teams = ['toro_rosso', 'force_india', 'racing_point']
    df = df[~df['constructorId'].isin(discontinued_teams)]
    return df

def load_driver_info():
    """Loads the driver information from CSV."""
    file_path = os.path.join(os.path.dirname(__name__), '.', 'Datasets', 'driver_info.csv')
    df_driver_info = pd.read_csv(file_path)
    df_driver_info['dateOfBirth'] = pd.to_datetime(df_driver_info['dateOfBirth'])
    return df_driver_info

def get_merged_race_driver_data():
    """Merges race results with driver info and calculates driver age at each race."""
    df_race_results = load_race_results_data()
    df_driver_info = load_driver_info()
    
    df_merged = pd.merge(df_race_results, df_driver_info[['driverId', 'dateOfBirth']], on='driverId')
    
    df_merged['date'] = pd.to_datetime(df_merged['date'])
    
    df_merged['age_at_race'] = (df_merged['date'] - df_merged['dateOfBirth']).dt.days / 365
    
    return df_merged

def plot_grid_vs_position(season_range):
    """Creates a scatter plot showing the relationship between grid start and final position for a range of seasons."""
    
    df_race_results = load_race_results_data()

    df_filtered = df_race_results[(df_race_results['season'] >= season_range[0]) & (df_race_results['season'] <= season_range[1])]

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

    fig = px.scatter(
        df_filtered,
        x='grid',
        y='position',
        color='constructorId',
        hover_data=['driverId', 'raceName', 'points'],
        labels={'grid': 'Grid Start', 'position': 'Final Position'},
        color_discrete_map=brand_colors
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        xaxis=dict(title='Grid Start', autorange='reversed', range=[0, 20]),
        yaxis=dict(title='Final Position', autorange='reversed', range=[1, 20]),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    return fig

def plot_mechanical_issues(selected_season_range):
    file_path = os.path.join(os.path.dirname(__name__), '.', 'Datasets', 'finishing_status_mechanica_issues_2017_2024.csv')
    df_mechanical_issues = pd.read_csv(file_path)
    total_occurrences = df_mechanical_issues['count'].sum()
    df_mechanical_issues['percentage'] = (df_mechanical_issues['count'] / total_occurrences) * 100
    threshold = 2.0
    df_mechanical_issues['status_grouped'] = df_mechanical_issues.apply(
        lambda row: row['status'] if row['percentage'] >= threshold else 'Other', axis=1
    )
    df_mechanical_issues_grouped = df_mechanical_issues.groupby('status_grouped').agg(
        {'count': 'sum', 'percentage': 'sum'}
        ).reset_index()
    df_top_mechanical_issues = df_mechanical_issues_grouped[(df_mechanical_issues_grouped['percentage'] >= 5.0) & 
                                                        (df_mechanical_issues_grouped['status_grouped'] != 'Other')]
    
    fig_pie = px.pie(df_mechanical_issues_grouped, 
             values='percentage', 
             names='status_grouped', 
             hole=0.5,
             hover_data=['count'],
             labels={'percentage':'Percentage'}
            )

    fig_pie.update_traces(textinfo='percent+label', textfont_size=12,
                      hovertemplate='<b>%{label}</b><br>Occurrences: %{customdata[0]}<br>Percentage: %{value:.2f}%')
    fig_pie.update_layout(showlegend=True, paper_bgcolor='lightgray')
    
    df_race_results = load_race_results_data()
    df_filtered = df_race_results[(df_race_results['season'] >= selected_season_range[0]) & 
                              (df_race_results['season'] <= selected_season_range[1])]
    top_issues = df_top_mechanical_issues['status_grouped'].tolist()
    df_filtered = df_filtered[df_filtered['status'].isin(top_issues)]
    df_grouped = df_filtered.groupby(['season', 'constructorId', 'status']).size().reset_index(name='count')
    df_pivot = df_grouped.pivot_table(index=['constructorId', 'season'], columns='status', values='count', fill_value=0).reset_index()
    df = pd.melt(df_pivot, id_vars=['constructorId', 'season'], var_name='issue', value_name='count')
    
    fig_stacked_bar = px.bar(df, 
                 x='constructorId', 
                 y='count', 
                 color='issue',
                 labels={'constructorId': 'Constructor', 'count': 'Issue Count'},
                 barmode='stack',
                 hover_data=['season'])
    
    fig_stacked_bar.update_layout(xaxis={'categoryorder': 'total descending'}, 
                      plot_bgcolor='white',
                      paper_bgcolor='lightgray')
    
    return fig_pie, fig_stacked_bar

def plot_avg_points_vs_age():
    """Plot average points per season against age."""
    df_driver_info = load_driver_info()
    df_merged = get_merged_race_driver_data()
    df_season_avg_points = df_merged.groupby(['driverId', 'season']).agg(
        avg_points=('points', 'mean'),
        first_race_date=('date', 'min'),
    ).reset_index()

    df_season_avg_points = pd.merge(df_season_avg_points, df_driver_info[['driverId', 'dateOfBirth']], on='driverId')
    df_season_avg_points['age_at_start_of_season'] = (pd.to_datetime(df_season_avg_points['first_race_date']) - 
                                                      pd.to_datetime(df_season_avg_points['dateOfBirth'])).dt.days / 365

    fig = px.scatter(df_season_avg_points, 
                     x='age_at_start_of_season', 
                     y='avg_points', 
                     labels={'age_at_start_of_season': 'Age at Start of Season', 'avg_points': 'Average Points'},
                     hover_data=['driverId', 'season'])
    fig.update_layout(margin=dict(l=50, r=50, t=80, b=50), showlegend=False, paper_bgcolor='lightgray')
    fig.update_traces(hovertemplate=(
        '<b>Driver ID:</b> %{customdata[0]}<br>' +
        '<b>Season:</b> %{customdata[1]}<br>' +
        '<b>Age at Start:</b> %{x:.1f}<br>' +
        '<b>Avg Point:</b> %{y:.1f}<br>'
    ))
    return fig

def plot_avg_position_vs_age():
    """Plot average position per season against age."""
    df_driver_info = load_driver_info()
    df_merged = get_merged_race_driver_data()
    df_season_avg_position = df_merged.groupby(['driverId', 'season']).agg(
        avg_position=('position', 'mean'),
        first_race_date=('date', 'min'),
    ).reset_index()

    df_season_avg_position = pd.merge(df_season_avg_position, df_driver_info[['driverId', 'dateOfBirth']], on='driverId')
    df_season_avg_position['age_at_start_of_season'] = (pd.to_datetime(df_season_avg_position['first_race_date']) - 
                                                        pd.to_datetime(df_season_avg_position['dateOfBirth'])).dt.days / 365

    fig = px.scatter(df_season_avg_position, 
                     x='age_at_start_of_season', 
                     y='avg_position', 
                     labels={'age_at_start_of_season': 'Age at Start of Season', 'avg_position': 'Average Position'},
                     hover_data=['driverId', 'season'])
    fig.update_yaxes(autorange='reversed', tickvals=[1, 5, 10, 15, 20])
    fig.update_layout(margin=dict(l=50, r=50, t=80, b=50), showlegend=False, paper_bgcolor='lightgray')
    fig.update_traces(hovertemplate=(
        '<b>Driver ID:</b> %{customdata[0]}<br>' +
        '<b>Season:</b> %{customdata[1]}<br>' +
        '<b>Age at Start:</b> %{x:.1f}<br>' +
        '<b>Avg Position:</b> %{y:.1f}<br>'
    ))
    return fig

def plot_avg_max_speed_vs_age():
    """Plot average max speed per season against age."""
    df_driver_info = load_driver_info()
    df_merged = get_merged_race_driver_data()
    df_season_avg_speed = df_merged.groupby(['driverId', 'season']).agg(
        avg_max_speed=('Max Avg Speed', 'mean'),
        first_race_date=('date', 'min'),
    ).reset_index()

    df_season_avg_speed = pd.merge(df_season_avg_speed, df_driver_info[['driverId', 'dateOfBirth']], on='driverId')
    df_season_avg_speed['age_at_start_of_season'] = (pd.to_datetime(df_season_avg_speed['first_race_date']) - 
                                                     pd.to_datetime(df_season_avg_speed['dateOfBirth'])).dt.days / 365

    fig = px.scatter(df_season_avg_speed, 
                     x='age_at_start_of_season',
                     y='avg_max_speed',
                     labels={'age_at_start_of_season': 'Age at Start of Season', 'avg_max_speed': 'Average Max Speed (km/h)'},
                     hover_data=['driverId', 'season'])
    
    fig.update_layout(margin=dict(l=50, r=50, t=80, b=50), showlegend=False, paper_bgcolor='lightgray')
    fig.update_traces(hovertemplate=(
        '<b>Driver ID:</b> %{customdata[0]}<br>' +
        '<b>Season:</b> %{customdata[1]}<br>' +
        '<b>Age at Start:</b> %{x:.1f}<br>' +
        '<b>Avg Max Speed:</b> %{y:.1f}<br>'
    ))
    return fig

def plot_top_drivers_podiums(top_n=6, season_range=(2017, 2024)):
    """Plots a stacked bar chart showing podium counts for the top drivers over a specified season range."""
    df_race_results = load_race_results_data()
    
    df_filtered = df_race_results[(df_race_results['season'] >= season_range[0]) & 
                                  (df_race_results['season'] <= season_range[1])]
    
    df_podiums = df_filtered[df_filtered['position'].isin([1, 2, 3])]

    df_podium_counts = df_podiums.groupby(['driverId', 'position']).size().reset_index(name='count')

    df_total_podiums = df_podium_counts.groupby('driverId')['count'].sum().reset_index(name='total_podiums')
    top_drivers = df_total_podiums.nlargest(top_n, 'total_podiums')['driverId'].tolist()

    df_top_podiums = df_podium_counts[df_podium_counts['driverId'].isin(top_drivers)]
    
    df_top_podiums['position'] = df_top_podiums['position'].map({1: '1st', 2: '2nd', 3: '3rd'})
    
    fig = px.bar(df_top_podiums, 
                 x='driverId', 
                 y='count', 
                 color='position',
                 labels={'driverId': 'Driver', 'count': 'Podium Count'},
                 category_orders={'position': ['1st', '2nd', '3rd']},
                 color_discrete_map={'1st': '#FFD700', '2nd': '#C0C0C0', '3rd': '#CD7F32'},
                 barmode='stack')

    fig.update_xaxes(categoryorder='total ascending')

    fig.update_layout(xaxis_title='Driver', yaxis_title='Podium Count', 
                      plot_bgcolor='white', paper_bgcolor='lightgray')

    return fig

def plot_top_constructors_podiums(top_n=6, season_range=(2017, 2024)):
    """Plots a stacked bar chart showing podium counts for the top constructors over a specified season range."""
    df_race_results = load_race_results_data()
    
    df_filtered = df_race_results[(df_race_results['season'] >= season_range[0]) & 
                                  (df_race_results['season'] <= season_range[1])]
    
    df_podiums = df_filtered[df_filtered['position'].isin([1, 2, 3])]

    df_podium_counts = df_podiums.groupby(['constructorId', 'position']).size().reset_index(name='count')

    df_total_podiums = df_podium_counts.groupby('constructorId')['count'].sum().reset_index(name='total_podiums')
    top_constructors = df_total_podiums.nlargest(top_n, 'total_podiums')['constructorId'].tolist()

    df_top_podiums = df_podium_counts[df_podium_counts['constructorId'].isin(top_constructors)]
    
    df_top_podiums['position'] = df_top_podiums['position'].map({1: '1st', 2: '2nd', 3: '3rd'})
    
    fig = px.bar(df_top_podiums, 
                 x='constructorId', 
                 y='count', 
                 color='position',
                 labels={'constructorId': 'Constructor', 'count': 'Podium Count'},
                 category_orders={'position': ['1st', '2nd', '3rd']},
                 color_discrete_map={'1st': '#FFD700', '2nd': '#C0C0C0', '3rd': '#CD7F32'},
                 barmode='stack')

    fig.update_xaxes(categoryorder='total ascending')

    fig.update_layout(xaxis_title='Constructor', yaxis_title='Podium Count', 
                      plot_bgcolor='white', paper_bgcolor='lightgray')

    return fig

def plot_head_to_head_performance(df_race_results, year, constructor_id):
    """Plots head-to-head comparison of two drivers from the same constructor for a given year."""
    
    df_filtered = df_race_results[(df_race_results['season'] == year) & 
                                  (df_race_results['constructorId'] == constructor_id)]
    
    unique_drivers = df_filtered['driverId'].unique()
    if len(unique_drivers) < 2:
        return None, f"Less than 2 drivers found for {constructor_id} in {year}"
    
    driver1, driver2 = unique_drivers[:2]
    
    driver1_race_wins = driver2_race_wins = 0
    driver1_grid_wins = driver2_grid_wins = 0
    
    for _, race in df_filtered.groupby('round'):
        race_data = race[['driverId', 'position', 'grid']]
        race_driver1 = race_data[race_data['driverId'] == driver1]
        race_driver2 = race_data[race_data['driverId'] == driver2]
        
        if not race_driver1.empty and not race_driver2.empty:
            if race_driver1['position'].values[0] < race_driver2['position'].values[0]:
                driver1_race_wins += 1
            else:
                driver2_race_wins += 1
            
            if race_driver1['grid'].values[0] < race_driver2['grid'].values[0]:
                driver1_grid_wins += 1
            else:
                driver2_grid_wins += 1
    
    comparison_data = {
        'Metric': ['Race Position Wins', 'Race Position Wins', 'Grid Position Wins', 'Grid Position Wins'],
        'Driver': [driver1, driver2, driver1, driver2],
        'Count': [driver1_race_wins, driver2_race_wins, driver1_grid_wins, driver2_grid_wins]
    }
    df_comparison = pd.DataFrame(comparison_data)
    
    fig = px.bar(df_comparison, x='Metric', y='Count', color='Driver',
                 labels={'Count': 'Times Finished Ahead', 'Metric': 'Comparison'},
                 barmode='group')
    
    return fig, None