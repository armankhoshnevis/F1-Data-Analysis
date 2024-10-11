import plotly.express as px
import pandas as pd

def load_race_schedule_data():
    return pd.read_csv('race_schedule.csv')

def f1_circuit_world_map(year):
    df_race_schedule = load_race_schedule_data()
    df_filtered_by_year = df_race_schedule[df_race_schedule['season'] == year]

    fig = px.scatter_geo(df_filtered_by_year,
                         lat='location-lat',
                         lon='location-long',
                         hover_name='circuitName',
                         hover_data={
                             'raceName': True,
                             'location-locality': True,
                             'location-country': True,
                             'season': True,
                             'location-lat': False,
                             'location-long': False
                         },
                         title=f'F1 Circuits World Map - {year}',
                         projection='equirectangular')

    fig.update_traces(marker=dict(color='blue', size=10, opacity=0.85, line=dict(width=1, color='black')))
    
    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor='lightgray',
            showocean=True,
            oceancolor='lightblue',
            showcountries=True,
            countrycolor='white',
            showframe=False,
            coastlinecolor='black',
            projection_scale=1.2
        ),
        title={
            'text': f'F1 Circuits World Map - {year}',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        title_font=dict(size=24, color='darkblue'),
        margin=dict(l=0, r=0, t=50, b=0),
        
        hoverlabel=dict(
            bgcolor="lightyellow",
            font_size=14,
            font_family="Arial",
            font_color="black"
        )
    )
    
    return fig


def races_by_continent():
    """Creates a scatter_geo plot showing the number of F1 races per continent."""
    df_race_schedule = load_race_schedule_data()

    country_to_continent = {
        'Australia': 'Oceania',
        'China': 'Asia',
        'Bahrain': 'Asia',
        'Russia': 'Europe',
        'Spain': 'Europe',
        'Monaco': 'Europe',
        'Canada': 'North America',
        'Azerbaijan': 'Europe',
        'Austria': 'Europe',
        'UK': 'Europe',
        'Hungary': 'Europe',
        'Belgium': 'Europe',
        'Italy': 'Europe',
        'Singapore': 'Asia',
        'Malaysia': 'Asia',
        'Japan': 'Asia',
        'USA': 'North America',
        'Mexico': 'South America',
        'Brazil': 'South America', 
        'UAE': 'Asia',
        'France': 'Europe',
        'Germany': 'Europe',
        'Portugal': 'Europe',
        'Turkey': 'Europe',
        'Netherlands': 'Europe', 
        'Qatar': 'Asia',
        'Saudi Arabia': 'Asia',
        'United States': 'North America'
    }

    df_race_schedule['continent'] = df_race_schedule['location-country'].map(country_to_continent)

    continent_race_count = df_race_schedule.groupby('continent').size().reset_index(name='race_count')
    total_races = continent_race_count['race_count'].sum()
    continent_race_count['percentage'] = (continent_race_count['race_count'] / total_races) * 100

    continent_geo = {
        'Europe': {'lat': 54.5260, 'long': 15.2551},
        'Asia': {'lat': 34.0479, 'long': 100.6197},
        'North America': {'lat': 47.875, 'long': -105.2551},
        'South America': {'lat': -8.7832, 'long': -55.4915},
        'Oceania': {'lat': -22.7359, 'long': 140.0188},
    }
    
    continent_race_count['lat'] = continent_race_count['continent'].map(lambda x: continent_geo[x]['lat'])
    continent_race_count['long'] = continent_race_count['continent'].map(lambda x: continent_geo[x]['long'])

    fig = px.scatter_geo(continent_race_count,
                         lat='lat',
                         lon='long',
                         hover_name='continent',
                         hover_data={'lat': False, 'long': False, 'race_count': True, 'percentage': ':.2f'},
                         size='race_count',
                         size_max=20,
                         color='race_count',
                         title='Number and Percentage of F1 Races by Continent (2017-2024)',
                         projection='equirectangular',
                         color_continuous_scale=px.colors.sequential.Plasma)

    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor='lightgray',
            showocean=True,
            oceancolor='lightblue',
            showcountries=True,
            countrycolor='white',
            showframe=False,
            coastlinecolor='black',
            projection_scale=1.2
        ),
        title={
        'text': 'F1 Races in Different Continents (2017-2024)',
        'x': 0.40,
        'xanchor': 'center',
        'yanchor': 'top'
    },
        title_font=dict(size=24, color='darkblue'),
        margin=dict(l=0, r=0, t=50, b=0),
        hoverlabel=dict(
            bgcolor="lightyellow",
            font_size=14,
            font_family="Arial",
            font_color="black"
        )
    )

    return fig

def races_by_circuit(start_year=2017, end_year=2024):
    """Creates a bar chart showing the number of races by circuit for a specified year range."""
    df_race_schedule = load_race_schedule_data()

    df_filtered = df_race_schedule[(df_race_schedule['season'] >= start_year) & (df_race_schedule['season'] <= end_year)]
 
    circuit_race_count = df_filtered.groupby('circuitName').size().reset_index(name='count')
    circuit_race_count = circuit_race_count.sort_values(by='count', ascending=False)

    fig = px.bar(
        circuit_race_count, 
        x='count',
        y='circuitName',
        title=f'Races by Circuit ({start_year}-{end_year})',
        hover_data={'circuitName': True, 'count': True},
        labels={'count': 'Number of Races', 'circuitName': 'Circuit'},
        color='count',
        color_continuous_scale=px.colors.sequential.Viridis,
        text='count'
    )
    
    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'font': dict(size=24, color='darkblue')},
        xaxis=dict(title='Number of Races', showgrid=False, tickfont=dict(size=14, color='black'), titlefont=dict(size=16, color='black')),
        yaxis=dict(title='Circuit', showgrid=False, tickfont=dict(size=14, color='black'), titlefont=dict(size=16, color='black')),
        plot_bgcolor='white',
        margin=dict(l=200, r=50, t=80, b=50),
        hoverlabel=dict(bgcolor="lightyellow", font_size=14, font_family="Arial", font_color="black"),
        height=800,
        coloraxis_showscale=False
    )

    fig.update_traces(textposition='outside')

    return fig

def races_by_country(start_year=2017, end_year=2024):
    """Creates a bar chart showing the number of races by country for a specified year range."""
    df_race_schedule = load_race_schedule_data()

    df_race_schedule = df_race_schedule[(df_race_schedule['season'] >= start_year) & (df_race_schedule['season'] <= end_year)]
    
    df_race_schedule['location-country'] = df_race_schedule['location-country'].replace({'United States': 'USA'})
    
    race_count_by_country = df_race_schedule.groupby('location-country').size().reset_index(name='count')
    race_count_by_country = race_count_by_country.sort_values(by='count', ascending=False)

    fig = px.bar(race_count_by_country, 
                 x='count',
                 y='location-country',
                 title=f'Races by Country ({start_year}-{end_year})',
                 hover_data={'location-country': True, 'count': True},
                 labels={'count': 'Number of Races', 'location-country': 'Country'},
                 color='count',
                 color_continuous_scale=px.colors.sequential.Viridis,
                 text='count')

    fig.update_layout(
        title={'x': 0.5, 'xanchor': 'center', 'font': dict(size=24, color='darkblue')},
        xaxis=dict(title='Number of Races', showgrid=False, tickfont=dict(size=14, color='black'), titlefont=dict(size=16, color='black')),
        yaxis=dict(title='Country', showgrid=False, tickfont=dict(size=14, color='black'), titlefont=dict(size=16, color='black')),
        plot_bgcolor='white',
        margin=dict(l=200, r=50, t=80, b=50),
        hoverlabel=dict(bgcolor="lightyellow", font_size=14, font_family="Arial", font_color="black"),
        height=800,
        coloraxis_showscale=False
    )

    fig.update_traces(textposition='outside')

    return fig