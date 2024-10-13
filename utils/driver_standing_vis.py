import plotly.express as px
import pandas as pd

def load_driver_standings_data():
    """Loads and updates the driver standings data."""
    df = pd.read_csv('driver_standings.csv')

    df['constructorId'] = df['constructorId'].replace({'alphatauri': 'rb'})
    df['constructorName'] = df['constructorName'].replace({'AlphaTauri': 'RB F1 Team'})
    
    return df

def plot_top_drivers_by_points(top=10):
    """Creates a bar chart for the top 10 drivers with the highest total points (2017-2024) using Viridis color scale."""
    
    df_driver_standings = load_driver_standings_data()

    df_driver_standings = df_driver_standings[df_driver_standings['season'].between(2017, 2024)]

    total_points_per_driver = df_driver_standings.groupby('driverId')['points'].sum().reset_index()

    top_drivers = total_points_per_driver.sort_values(by='points', ascending=False).head(top)

    fig = px.bar(
        top_drivers,
        x='driverId',
        y='points',
        labels={'driverId': 'Driver', 'points': 'Total Points'},
        text='points',
        color='points',
        color_continuous_scale='Viridis'
    )

    fig.update_layout(
        xaxis=dict(title='Driver', tickfont=dict(size=12), autorange='reversed'),
        yaxis=dict(title='Total Points', tickfont=dict(size=12)),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')

    return fig

def plot_top_drivers_by_wins(top=10):
    """Creates a bar chart for the top 10 drivers with the most wins (2017-2024) using Viridis color scale."""
    
    df_driver_standings = load_driver_standings_data()

    total_wins_per_driver = df_driver_standings.groupby('driverId')['wins'].sum().reset_index()

    top_drivers = total_wins_per_driver.sort_values(by='wins', ascending=False).head(top)

    fig = px.bar(
        top_drivers,
        x='driverId',
        y='wins',
        labels={'driverId': 'Driver', 'wins': 'Number of Wins'},
        text='wins',
        color='wins',
        color_continuous_scale='Viridis'
    )

    fig.update_layout(
        xaxis=dict(title='Driver', tickfont=dict(size=12), autorange='reversed'),
        yaxis=dict(title='Number of Wins', tickfont=dict(size=12)),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')

    return fig

def plot_driver_progression(driver_id):
    """Creates three visualizations for a specific driver: Points vs Year, Wins vs Year, Standing vs Year (reversed)."""
    
    df_driver_standings = load_driver_standings_data()

    df_driver = df_driver_standings[df_driver_standings['driverId'] == driver_id]

    fig_points = px.line(
        df_driver,
        x='season',
        y='points',
        labels={'season': 'Year', 'points': 'Points'},
        markers=True
    )
    fig_points.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        margin=dict(l=50, r=50, t=50, b=50),
    )

    fig_wins = px.line(
        df_driver,
        x='season',
        y='wins',
        labels={'season': 'Year', 'wins': 'Number of Wins'},
        markers=True
    )
    fig_wins.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        margin=dict(l=50, r=50, t=50, b=50),
    )

    fig_standing = px.line(
        df_driver,
        x='season',
        y='position',
        labels={'season': 'Year', 'position': 'Position'},
        markers=True
    )
    fig_standing.update_layout(
        yaxis=dict(autorange='reversed'),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        margin=dict(l=50, r=50, t=50, b=50),
    )

    return fig_points, fig_wins, fig_standing