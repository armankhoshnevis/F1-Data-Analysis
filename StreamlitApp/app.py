import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.race_schedule_vis import (
    f1_circuit_world_map,
    races_by_continent,
    races_by_circuit,
    races_by_country
    )

from utils.constructor_standing_vis import (
    plot_constructor_ranking_vs_year,
    plot_constructor_wins_vs_year,
    plot_constructor_points_vs_year,
    plot_constructor_points_distribution_per_year,
    plot_overall_win_percentage,
    plot_yearly_win_percentage
    )

from utils.driver_standing_vis import (
    load_driver_standings_data, 
    plot_driver_progression, 
    plot_top_drivers_by_points, 
    plot_top_drivers_by_wins
    )


from utils.race_results_vis import (
    load_race_results_data,
    plot_grid_vs_position, 
    plot_mechanical_issues,
    get_merged_race_driver_data,
    plot_avg_points_vs_age,
    plot_avg_position_vs_age,
    plot_avg_max_speed_vs_age,
    plot_top_constructors_podiums,
    plot_top_drivers_podiums,
    plot_head_to_head_performance
)

st.set_page_config(
    page_title="FDS Project - F1",
    page_icon="f1logo.png",
    layout="wide",
)

# Sidebar for EDA section
st.sidebar.title("F1 Data Analysis")

# EDA Sections
eda_section = st.sidebar.selectbox("Select Section", ["Introduction", "Race Circuits", "Constructor Standing", "Driver Standing", "Race Results", "Pit Stops"])

# Race Circuits Subsection
if eda_section == "Introduction":
    image_path = os.path.join(os.path.dirname(__file__), "DALLE_2024_10_10.webp")
    st.image(image_path, caption="AI-Generated Picture, DALL·E, 2024-10-10", use_column_width=True)
    st.markdown("""
                ### Hello F1
                
                Formula One, or F1, stands as the world's most elite motorsport league. It is not only about the
                drivers battling for the championship but also about the constructors, supported by a vast team of
                designers, manufacturers, engineers, data scientists, AI specialists, and more, all competing for
                the constructors' championship. In many ways, this is truly a "league of nerds" as well!

                Each F1 season, which spans roughly nine months, features 24 races known as Grands Prix, where 20
                drivers from 10 teams compete against each other. During each race, lap, sector, and corner, an
                enormous amount of data is collected by car sensors and transmitted to various engineering teams.
                This data enables the teams to fine-tune car settings, introduce updates throughout the season, 
                and prepare the best possible car for the following year.

                In today's world of data and AI, F1 is no exception. As James Vowles, Team Principal of Williams
                Racing, aptly put it, “Data, for me, is the foundation of F1. There's no human judgment involved.
                You've got to get your foundation right in data.” In this analysis, powered by the renowned Ergast
                API, we delve into different aspects of F1 to gain a clearer, more profound understanding of 
                driver and constructor performance, along with the many factors influencing them.
                
                In this project, we are primarily focused on the "Hybrid Era" of Formula 1, which began in 2014 with the
                introduction of 1.6-liter V6 turbocharged hybrid power units. Emphasis is placed on data from 2017
                onwards, to account for the learning curve teams faced while adapting to hybrid engines and to
                observe the impact of the regulation changes in 2022, along with the dominance and team battles in
                recent years.
                
                Explore the data through interactive visualization tools on this website and uncover the dynamics
                of F1. Enjoy your journey into the world of data-driven motorsport!
                
                Prepared by Arman Khoshnevis (khoshne1@msu.edu), Fall 2024
                """)

elif eda_section == "Race Circuits":
    visualization = st.sidebar.selectbox(
        "Select Visualization",
        ["World Map (F1 Circuits)", "Races by Continent", "Races by Circuit/Country"]
    )
    if visualization == "World Map (F1 Circuits)":
        year = st.sidebar.selectbox("Select Year", options=[2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017])
        fig = f1_circuit_world_map(year)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
                    Here, you can see the global distribution of Formula 1 circuits for a selected year.
                    Each marker highlights a race location, with details on the circuit and country.
                    The map emphasizes the diverse environmental conditions, that teams must adapt to for optimal
                    performance. These variations influence car setup and driver preparation, 
                    underscoring the logistical challenges teams face in navigating the season's unique demands.
                    """
        )
    
    elif visualization == "Races by Continent":
        fig = races_by_continent()
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
                    This visualization illustrates the distribution of Formula 1 races by continent over the past
                    several seasons. Europe holds the largest share of the calendar each year, emphasizing its
                    historical and ongoing importance in F1. Asia and the Middle East follow closely, reflecting 
                    the sport's expansion into new regions. North and South America account for fewer races,
                    yet play a critical role in rounding out the global F1 season. Each continent’s race count is
                    shown in terms of absolute numbers and percentages, highlighting their relative contributions.
                    """
        )
    
    elif visualization == "Races by Circuit/Country":
        start_year, end_year = st.sidebar.select_slider(
            "Select Year Range",
            options=list(range(2017, 2025)),
            value=(2017, 2024)
        )
        y_axis_choice = st.sidebar.selectbox(
            "Select Y-Axis",
            options=["Circuit", "Country"]
        )
        if y_axis_choice == "Circuit":
            fig = races_by_circuit(start_year=start_year, end_year=end_year)
        elif y_axis_choice == "Country":
            fig = races_by_country(start_year=start_year, end_year=end_year)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
                    This bar chart showcases the number of Formula 1 races held in each country/circuit over the
                    selected time frame. The visualization highlights the USA’s growing influence on the F1 
                    calendar, partially due to the attractive documentary named Drive to Survive by Netflix,
                    currently hosting three races each season in Austin, Miami, and Las Vegas. It also reflects
                    the enduring presence of classic circuits in countries such as Monaco, the UK, Hungary, and
                    Austria, which have consistently retained their places in the F1 schedule. Additionally, this
                    chart reveals countries that were once hosts but have since departed from the calendar,
                    underscoring F1's dynamic global footprint.
                    """)

elif eda_section == "Constructor Standing":
    st.subheader("Constructor Standing Visualizations")
    
    constructor_vis_option = st.sidebar.selectbox(
        "Select Visualization",
        ["Yearly Trends", "Dominance"]
    )
    
    if constructor_vis_option == "Yearly Trends":
        start_year, end_year = st.sidebar.select_slider(
            "Select Year Range",
            options=list(range(2017, 2025)),
            value=(2017, 2024)
        )
        
        show_ranking = st.sidebar.checkbox("Show Ranking vs Year", value=True)
        show_wins = st.sidebar.checkbox("Show Wins vs Year", value=True)
        show_points = st.sidebar.checkbox("Show Points vs Year", value=True)

        if show_ranking:
            st.write("### Ranking vs Year")
            fig_ranking = plot_constructor_ranking_vs_year(start_year=start_year, end_year=end_year)
            st.plotly_chart(fig_ranking, use_container_width=True)

        if show_wins:
            st.write("### Wins vs Year")
            fig_wins = plot_constructor_wins_vs_year(start_year=start_year, end_year=end_year)
            st.plotly_chart(fig_wins, use_container_width=True)

        if show_points:
            st.write("### Points vs Year")
            fig_points = plot_constructor_points_vs_year(start_year=start_year, end_year=end_year)
            st.plotly_chart(fig_points, use_container_width=True)
        
        st.markdown("""
                    These visualizations track constructor performance trends in rankings, wins, and points across
                    recent seasons. Mercedes' dominance is evident from 2017 to 2021, followed by the rise of
                    Red Bull, starting in 2021 and solidifying through 2023. By 2024, a closer championship battle
                    emerges between Red Bull, McLaren, Ferrari, and Mercedes, reflecting the impact of the 2022
                    regulation changes aimed at enhancing competition.

                    In the mid-to-lower rankings, Aston Martin has solidified a middle-ground position, with Haas
                    showing marked improvement. In contrast, Alpine has experienced a notable decline, continuing
                    from its rebranding of Renault in 2020-2021. Additionally, Alfa Romeo’s transition to Sauber
                    in 2023 further reshapes the grid's landscape, highlighting the evolving dynamics within the
                    constructor standings.
                    """)

    elif constructor_vis_option == "Dominance":
        st.write("### Points Distribution per Year")
        fig_points_dist = plot_constructor_points_distribution_per_year()
        st.plotly_chart(fig_points_dist, use_container_width=True)

        st.write("### Overall Win Percentage per Constructor")
        fig_overall_win_percentage = plot_overall_win_percentage()
        st.plotly_chart(fig_overall_win_percentage, use_container_width=True)

        st.write("### Year-by-Year Win Percentage per Constructor")
        fig_yearly_win_percentage = plot_yearly_win_percentage()
        st.plotly_chart(fig_yearly_win_percentage, use_container_width=True)
        
        st.markdown("""
                    The points distribution visualization provides a higher-level look into constructor dominance
                    each season. Notably, 2021 and 2023 show a wide range of high points, reflecting dominant
                    performances. In contrast, the 2024 season displays a much narrower distribution, indicating
                    a more competitive field.
                    
                    The overall and yearly win percentage charts further emphasize the shifts in constructor
                    dominance, highlighting how leading teams' win shares have evolved. Together, these
                    visualizations underscore the competitive dynamics and changes in the F1 landscape over recent
                    years.
                    """)

# Driver Standing Subsection
elif eda_section == "Driver Standing":
    st.subheader("Driver Standing Progression")
    visualization_option = st.sidebar.selectbox(
        "Select Visualization",
        ["Individual Driver Performance", "Top Drivers Over Years"]
    )

    if visualization_option == "Individual Driver Performance":
        df_driver_standings = load_driver_standings_data()
        unique_drivers = sorted(df_driver_standings['driverId'].unique())
        selected_driver = st.sidebar.selectbox("Select Driver", options=unique_drivers)

        # Checkboxes for controlling which plots to show
        show_points = st.sidebar.checkbox("Show Points vs Year", value=True)
        show_wins = st.sidebar.checkbox("Show Wins vs Year", value=True)
        show_standing = st.sidebar.checkbox("Show Standing vs Year", value=True)

        fig_points, fig_wins, fig_standing = plot_driver_progression(selected_driver)
        
        if fig_points and show_points:
            st.write("### Points vs Year")
            st.plotly_chart(fig_points, use_container_width=True)

        if fig_wins and show_wins:
            st.write("### Wins vs Year")
            st.plotly_chart(fig_wins, use_container_width=True)

        if fig_standing and show_standing:
            st.write("### Standing vs Year")
            st.plotly_chart(fig_standing, use_container_width=True)

        st.markdown("""
                    In this section, feel free to check different drivers and look into their higher-level aspects
                    of performance over years! The drivers' list is pretty comprehensive. You probably endup 
                    finding your favorite driver or drivers' of your favorite team. Who do you think is going to
                    the next new world champion? Lando Norris? Charles Leclerc? George Russell? ...
                    """)
        
    elif visualization_option == "Top Drivers Over Years":
        top_n = st.sidebar.number_input("Select number of top drivers", min_value=1, max_value=20, value=10)
        fig_top_drivers_by_points = plot_top_drivers_by_points(top=top_n)
        fig_top_drivers_by_wins = plot_top_drivers_by_wins(top=top_n)
        st.write("### By points")
        st.plotly_chart(fig_top_drivers_by_points, use_container_width=True)
        st.write("### By Wins")
        st.plotly_chart(fig_top_drivers_by_wins, use_container_width=True)
        st.markdown("""
                    Here, you can clearly see the brutal dominance of Lewis Hamilton and Max Verstappen over other drivers from
                    Mercedes and Red bull, respectively. You can also see drivers who are close to the end of
                    their career, but given their previous or current team, they could manage to collect points
                    and wins. 
                    
                    Interestingly, Sebastian Vettel, who retired at the end of 2022 season, and who
                    has not been in good shape in the past couple of years and he is currently without team is
                    also in the figures as they had previously showed a tremendous performance.
                    """)

# Race Results Subsection
elif eda_section == "Race Results":
    st.subheader("Race Results Visualizations")
    
    race_result_visualization = st.sidebar.selectbox(
        "Select Visualization",
        ["Grid Start vs Final Position", "Mechanical Issues", "Age-Based Performance", 
         "Podium Counts", "Driver's Head-to-Head Performance", "Lap Times"]
    )
    
    if race_result_visualization == "Grid Start vs Final Position":
        df_race_results = load_race_results_data()
        min_season = int(df_race_results['season'].min())
        max_season = int(df_race_results['season'].max())
        selected_season_range = st.sidebar.slider(
            "Select Season Range",
            min_value=min_season,
            max_value=max_season,
            value=(min_season, max_season)
        )
        st.write(f"### Impact of Grid Start on Final Position ({selected_season_range[0]} - {selected_season_range[1]})")
        fig_grid_vs_position = plot_grid_vs_position(selected_season_range)
        st.plotly_chart(fig_grid_vs_position, use_container_width=True)
        st.markdown("""
                    This scatter plot highlights the relationship between drivers' starting grid positions and 
                    their final race positions across selected seasons. Generally, starting higher on the grid
                    correlates with finishing in a better position, with many drivers either maintaining or
                    improving their positions. However, qualifying (starting grid position) results are not the
                    only effective parameter. Moreover, some weird data points are visible, such as cases where
                    drivers started from the pit lane (indicated by a grid position of zero) or were disqualified.

                    As the season range expands, this correlation may become less distinct, reflecting the 
                    unpredictability of F1 races and the various factors that can impact race outcomes.
                    """)

    elif race_result_visualization == "Mechanical Issues":
        df_race_results = load_race_results_data()
        min_season = int(df_race_results['season'].min())
        max_season = int(df_race_results['season'].max())
        selected_season_range = st.sidebar.slider(
            "Select Season Range",
            min_value=min_season,
            max_value=max_season,
            value=(min_season, max_season)
        )
        st.write(f"### Top Mechanical Issues by Constructor ({selected_season_range[0]} - {selected_season_range[1]})")
        fig_pie, fig_stacked_bar = plot_mechanical_issues(selected_season_range)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.write(f"### Constructors Reliability ({selected_season_range[0]} - {selected_season_range[1]})")
        st.plotly_chart(fig_stacked_bar, use_container_width=True)
        st.markdown("""
                    The pie chart illustrates the most common mechanical failures faced by constructors over the
                    years. Beyond the engine, which is the core of any F1 car, brakes, power units, gearboxes, and
                    hydraulic systems also emerge as critical areas requiring meticulous design and maintenance.
                    The 'Other' category, comprising roughly 22%, underscores the variety of components that can
                    fail, reflecting the complexity of F1 vehicles.

                    The stacked bar chart further explores constructors' reliability over time, revealing how
                    mechanical issues have impacted different teams throughout specific periods. This
                    visualization captures the variability in how teams address and evolve their cars' reliability
                    in response to these ongoing challenges.
                    """)
    
    elif race_result_visualization == "Age-Based Performance":
        
        age_performance_vis = st.sidebar.selectbox(
            "Select Performance Metric",
            ["Average Points vs Age", "Average Position vs Age", "Average Max Speed vs Age"]
        )
        
        df_merged = get_merged_race_driver_data()
        
        if age_performance_vis == "Average Points vs Age":
            fig_avg_points = plot_avg_points_vs_age()
            st.plotly_chart(fig_avg_points, use_container_width=True)

        elif age_performance_vis == "Average Position vs Age":
            fig_avg_position = plot_avg_position_vs_age()
            st.plotly_chart(fig_avg_position, use_container_width=True)

        elif age_performance_vis == "Average Max Speed vs Age":
            fig_avg_max_speed = plot_avg_max_speed_vs_age()
            st.plotly_chart(fig_avg_max_speed, use_container_width=True)
        
        st.markdown("""
                    These scatter plots display the relationship between drivers' ages and their average points,
                    positions, and maximum speeds across seasons. While it's generally expected that driver
                    performance declines as they surpass a certain age, the data reveals that this trend is not as
                    pronounced today. This resilience can be attributed to modern drivers' commitment to rigorous
                    training, professional lifestyles, and mental discipline, allowing them to maintain 
                    competitive performance even as they age.
                    """)
    
    elif race_result_visualization == "Podium Counts":
        podium_option = st.sidebar.selectbox(
            "Podium Counts for:",
            ["Drivers", "Constructors"]
        )
        top_n = st.sidebar.number_input("Select number of top performers", min_value=1, max_value=20, value=6)
        df_race_results = load_race_results_data()
        min_season = int(df_race_results['season'].min())
        max_season = int(df_race_results['season'].max())
        selected_season_range = st.sidebar.slider(
            "Select Season Range",
            min_value=min_season,
            max_value=max_season,
            value=(min_season, max_season)
        )
        if podium_option == "Drivers":
            st.write(f"### Top {top_n} Drivers Podium Count ({selected_season_range[0]} - {selected_season_range[1]})")
            fig_top_drivers_podiums = plot_top_drivers_podiums(top_n=top_n, season_range=selected_season_range)
            st.plotly_chart(fig_top_drivers_podiums, use_container_width=True)
        elif podium_option == "Constructors":
            st.write(f"### Top {top_n} Constructors Podium Count ({selected_season_range[0]} - {selected_season_range[1]})")
            fig_top_constructors_podiums = plot_top_constructors_podiums(top_n=top_n, season_range=selected_season_range)
            st.plotly_chart(fig_top_constructors_podiums, use_container_width=True)
        st.markdown("""
                    These stacked bar charts offer a detailed look at the performance of top drivers and
                    constructors based on their podium finishes (1st, 2nd, and 3rd places). By adjusting the year
                    range and number of top performers displayed, you can explore the evolving landscape of 
                    dominance in Formula 1. This dynamic visualization provides insights into how certain drivers 
                    and teams consistently secure podium finishes, reflecting their competitive edge across seasons.
                    """)
        
    elif race_result_visualization == "Driver's Head-to-Head Performance":
        df_race_results = load_race_results_data()
        
        selected_season = st.sidebar.selectbox("Select Season", options=sorted(df_race_results['season'].unique(), reverse=True))
        
        constructors_in_season = sorted(df_race_results[df_race_results['season'] == selected_season]['constructorId'].unique())
        selected_constructor = st.sidebar.selectbox("Select Constructor", options=constructors_in_season)
        
        st.write(f"### Head-to-Head Performance for {selected_constructor} in {selected_season}")
        fig_head_to_head, error = plot_head_to_head_performance(df_race_results, year=selected_season, constructor_id=selected_constructor)
        
        if fig_head_to_head:
            st.plotly_chart(fig_head_to_head, use_container_width=True)
        else:
            st.write(error)
        st.markdown("""
                    This bar chart provides a head-to-head comparison between two drivers from the same
                    constructor over a selected season. It highlights each driver's performance in terms of
                    finishing position and grid position, revealing who consistently finishes ahead. Intra-team
                    comparisons like this are a critical factor in assessing a driver's standing within the team.
                    Underperforming compared to a teammate can intensify pressure on drivers, as teams often use
                    these comparisons to evaluate a driver's ability to maximize the car's potential.
                    """)
    
    elif race_result_visualization == "Lap Times":
        lap_times_df = load_lap_times_data()
        
        selected_season = st.sidebar.selectbox("Select Season", options=sorted(lap_times_df['season'].unique(), reverse=True))
        rounds_in_season = lap_times_df[lap_times_df['season'] == selected_season]['round'].unique()
        selected_round = st.sidebar.selectbox("Select Round", options=sorted(rounds_in_season))
        
        lower_percentile = st.sidebar.slider("Lower Percentile", 0, 50, 5)
        upper_percentile = st.sidebar.slider("Upper Percentile", 50, 100, 95)
        
        st.write(f"### Lap Times Box Plot for Season {selected_season}, Round {selected_round}")
        fig_lap_times = plot_driver_lap_times(selected_season, selected_round, lower_percentile, upper_percentile)
        st.plotly_chart(fig_lap_times, use_container_width=True)
        st.markdown("""
                    This box plot visualizes the lap times of all drivers for a selected race, with adjustable lower and upper
                    limits to filter out extreme outliers (such as laps with pit stops or a safty car). By focusing
                    on the middle range of lap times, this visualization provides a clearer view of each driver's
                    performance consistency. 
                    """)

