# Foundation of Data Science (CMSE 830 - MSU) - MidTerm Project: F1 Data Analysis

In this project, we are primarily focused on the data analysis of the "Hybrid Era" of Formula 1, which began in 2014 with the introduction of 1.6-liter V6 turbocharged hybrid power units. Emphasis is placed on data from 2017 onwards, to account for the learning curve teams faced while adapting to hybrid engines and to observe the impact of the regulation changes in 2022, along with the dominance and team battles in recent years.

Each directory in this repository is described as follows:

**Datasets**:

The Ergast API (https://ergast.com/mrd/) is utilized for collecting the datasets corresponding to different aspects of the F1 races corresponding the year range from 2017 to 2024 (Round 18, Singapore Grand Prix). The Ergast Developer API is an experimental web service which provides a historical record of motor racing data for non-commercial purposes. The API provides data for the Formula 1 series, from the beginning of the world championships in 1950.
In this directory you can find the collected data in the csv format. Also, Fetch_Data.ipynb provides the codes used for downloading the data from the API. These csv files are used for visualization purposes.

**ImputationAttempt**:

Here, I tried to impute the missing lap times for dirves with DNF (Did Not Finish) status. DNF referrs to whatever reason that the driver could not finish the race and as a result, no lap time is recorded. In a sesne, this is not truly missingness issue because the driver did not finish the race in the frist place! However, this is an attempt of filling the lap times for the missing laps based on the lap times the driver had in his record in the previous years in the same circuit!

**StreamlitApp**:

This directory contains the app.py code which is linked to the Streamlit for deploying the website corresponding to this project. Inside this app, all the visualization functions that are provided in the utils directory are imported first. This app is designed to be as interactive as possible so that users can explore the data more in depth and gain more understanding. The web app is hopefully accessible via this [link] (https://fdsmidterm-n9bhczdbje5okeen3vs5j4.streamlit.app/)!

**utils**:

Inside this directory, all the visualizations functions corresponding to the plots/graphs embedded in the Streamlit website is provided. It should be noted that the relative address to the each required dataset (.csv file) is declared as required. Be mindful of this note if you want to clone the repository. Furthermore, to explore how does each visualization function work, you can copy paste the function of interest (plus the necessary load_data functions) into a Jupyter notebook. Then call the function and display the visualization using .show() command.

**Notes**:

I replace alphatauri team with rb and remove the discontinued teams toro_rosso, force_india, and racing_point to avoid introducing bias into the analysis.

In the requirements.txt, I have specified the version of the packages required for the Streamlit app to deploy the web page.
