import plotly.express as px
import pandas as pd

def load_constructor_standings_data():
    df = pd.read_csv('constructor_standings.csv')

    df['constructorId'] = df['constructorId'].replace({'alphatauri': 'rb'})
    df['constructorName'] = df['constructorName'].replace({'AlphaTauri': 'RB F1 Team'})
    
    return df

def plot_constructor_ranking_vs_year(start_year=2017, end_year=2024):
    """Creates a line chart for Constructor Ranking vs Year, excluding discontinued teams, within a specified year range."""
    
    df_constructor_standings = load_constructor_standings_data()

    discontinued_teams = ['toro_rosso', 'force_india', 'racing_point']
    df_constructor_standings = df_constructor_standings[~df_constructor_standings['constructorId'].isin(discontinued_teams)]

    df_constructor_standings = df_constructor_standings[
        (df_constructor_standings['season'] >= start_year) &
        (df_constructor_standings['season'] <= end_year)
    ]

    df_constructor_standings['season'] = df_constructor_standings['season'].astype(int)
    df_constructor_standings['position'] = df_constructor_standings['position'].astype(int)

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

    fig = px.line(
        df_constructor_standings,
        x='season',
        y='position',
        color='constructorId',
        labels={
            'season': 'Year',
            'position': 'Ranking',
            'constructorId': 'Constructor'
        },
        markers=True,
        color_discrete_map=brand_colors
    )

    fig.update_yaxes(autorange="reversed", tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    fig.update_layout(
        xaxis=dict(title='Year', tickfont=dict(size=12), tickvals=list(range(start_year, end_year + 1))),
        yaxis=dict(title='Ranking', tickfont=dict(size=12)),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    return fig

def plot_constructor_wins_vs_year(start_year=2017, end_year=2024):
    """Creates a line chart for Number of Wins vs Year within a specified range."""
    
    df_constructor_standings = load_constructor_standings_data()

    discontinued_teams = ['toro_rosso', 'force_india', 'racing_point']
    df_constructor_standings = df_constructor_standings[~df_constructor_standings['constructorId'].isin(discontinued_teams)]

    df_constructor_standings['season'] = df_constructor_standings['season'].astype(int)
    df_constructor_standings['wins'] = df_constructor_standings['wins'].astype(int)
    
    df_filtered = df_constructor_standings[(df_constructor_standings['season'] >= start_year) & 
                                           (df_constructor_standings['season'] <= end_year)]

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

    fig = px.line(
        df_filtered,
        x='season',
        y='wins',
        color='constructorId',
        labels={
            'season': 'Year',
            'wins': 'Number of Wins',
            'constructorId': 'Constructor'
        },
        markers=True,
        color_discrete_map=brand_colors
    )

    fig.update_layout(
        xaxis=dict(title='Year', tickfont=dict(size=12), tickvals=list(range(start_year, end_year + 1))),
        yaxis=dict(title='Number of Wins', tickfont=dict(size=12)),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    return fig

def plot_constructor_points_vs_year(start_year=2017, end_year=2024):
    """Creates a line chart for Points vs Year for each constructor within a specified range."""
    
    df_constructor_standings = load_constructor_standings_data()

    discontinued_teams = ['toro_rosso', 'force_india', 'racing_point']
    df_constructor_standings = df_constructor_standings[~df_constructor_standings['constructorId'].isin(discontinued_teams)]

    df_constructor_standings['season'] = df_constructor_standings['season'].astype(int)
    df_constructor_standings['points'] = df_constructor_standings['points'].astype(float)
    
    # Filter data within the selected year range
    df_filtered = df_constructor_standings[(df_constructor_standings['season'] >= start_year) & 
                                           (df_constructor_standings['season'] <= end_year)]

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

    fig = px.line(
        df_filtered,
        x='season',
        y='points',
        color='constructorId',
        labels={
            'season': 'Year',
            'points': 'Points',
            'constructorId': 'Constructor'
        },
        markers=True,
        color_discrete_map=brand_colors
    )

    fig.update_layout(
        xaxis=dict(title='Year', tickfont=dict(size=12), tickvals=list(range(start_year, end_year + 1))),
        yaxis=dict(title='Points', tickfont=dict(size=12)),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    return fig

def plot_constructor_points_distribution_per_year():
    """Creates a box plot for the distribution of constructor points per year."""
    
    df_constructor_standings = load_constructor_standings_data()

    discontinued_teams = ['toro_rosso', 'force_india', 'racing_point']
    df_constructor_standings = df_constructor_standings[~df_constructor_standings['constructorId'].isin(discontinued_teams)]

    df_constructor_standings['season'] = df_constructor_standings['season'].astype(int)
    df_constructor_standings['points'] = df_constructor_standings['points'].astype(float)

    fig = px.box(
        df_constructor_standings,
        x='season',
        y='points',
        labels={
            'season': 'Year',
            'points': 'Points'
        }
    )

    fig.update_layout(
        xaxis=dict(title='Year', tickfont=dict(size=12)),
        yaxis=dict(title='Points', tickfont=dict(size=12)),
        plot_bgcolor='white',
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    return fig

def calculate_win_percentage(df):
    """Calculates overall and year-by-year win percentage for constructors and filters out zero-win and discontinued teams."""
    
    discontinued_teams = ['toro_rosso', 'force_india', 'racing_point']
    df = df[~df['constructorId'].isin(discontinued_teams)]

    overall_wins = df.groupby('constructorId')['wins'].sum().reset_index()
    overall_wins['win_percentage'] = (overall_wins['wins'] / overall_wins['wins'].sum()) * 100

    overall_wins = overall_wins[overall_wins['win_percentage'] > 0]
    
    overall_wins = overall_wins.sort_values(by='win_percentage', ascending=True)

    yearly_wins = df.groupby(['season', 'constructorId'])['wins'].sum().reset_index()
    yearly_races = df.groupby('season')['wins'].sum().reset_index().rename(columns={'wins': 'total_wins_per_year'})
    yearly_wins = yearly_wins.merge(yearly_races, on='season')
    yearly_wins['win_percentage'] = (yearly_wins['wins'] / yearly_wins['total_wins_per_year']) * 100

    yearly_wins = yearly_wins[yearly_wins['win_percentage'] > 0]

    return overall_wins, yearly_wins

def plot_overall_win_percentage():
    """Creates a bar chart for overall win percentage per constructor, excluding zero-win and discontinued teams."""
    df_constructor_standings = load_constructor_standings_data()
    overall_wins, _ = calculate_win_percentage(df_constructor_standings)
    
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
    
    fig = px.bar(
        overall_wins,
        x='constructorId',
        y='win_percentage',
        labels={'constructorId': 'Constructor', 'win_percentage': 'Win Percentage (%)'},
        text='win_percentage',
        color='constructorId',
        color_discrete_map=brand_colors
    )

    fig.update_layout(
        xaxis=dict(title='Constructor', tickfont=dict(size=12)),
        yaxis=dict(title='Win Percentage (%)', tickfont=dict(size=12)),
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"),
    )
    
    fig.update_traces(
        texttemplate='%{text:.2f}%',
        textposition='outside',
        hovertemplate='<b>Constructor:</b> %{x}<br>' +
                      '<b>Win Percentage:</b> %{y:.2f}%<extra></extra>'
    )

    return fig

def plot_yearly_win_percentage():
    """Creates a bar chart for yearly win percentage per constructor, excluding zero-win and discontinued teams."""
    df_constructor_standings = load_constructor_standings_data()
    _, yearly_wins = calculate_win_percentage(df_constructor_standings)

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
    
    fig = px.bar(
        yearly_wins,
        x='season',
        y='win_percentage',
        color='constructorId',
        barmode='group',
        labels={'season': 'Year', 'win_percentage': 'Win Percentage (%)', 'constructorId': 'Constructor'},
        color_discrete_map=brand_colors,
    )
    
    fig.update_layout(
        xaxis=dict(title='Year', tickfont=dict(size=12)),
        yaxis=dict(title='Win Percentage (%)', tickfont=dict(size=12)),
        plot_bgcolor='white',
        paper_bgcolor='lightgray',
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    
    fig.update_traces(
        hovertemplate='<b>Year:</b> %{x}<br>' +
                      '<b>Win Percentage:</b> %{y:.2f}%<extra></extra>',
        customdata=yearly_wins[['constructorId']].values
    )

    return fig