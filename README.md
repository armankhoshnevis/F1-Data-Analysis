# Foundation of Data Science (CMSE 830 - MSU) - MidTerm Project: F1 Data Analysis

In this project, we are primarily focused on the data analysis of the "Hybrid Era" of Formula 1, which began in 2014 with the introduction of 1.6-liter V6 turbocharged hybrid power units. Emphasis is placed on data from 2017 onwards, to account for the learning curve teams faced while adapting to hybrid engines and to observe the impact of the regulation changes in 2022, along with the dominance and team battles in recent years.

Each directory in this repository is described as follows:

Datasets:

The Ergast API (https://ergast.com/mrd/) is utilized for collecting the datasets corresponding to different aspects of the F1 races corresponding the year range from 2017 to 2024 (Round 18, Singapore Grand Prix). The Ergast Developer API is an experimental web service which provides a historical record of motor racing data for non-commercial purposes. The API provides data for the Formula 1 series, from the beginning of the world championships in 1950.
In this directory you can find the collected data in the csv format. Also, Fetch_Data.ipynb provides the codes used for downloading the data from the API. These csv files are used for visualization purposes.

StreamlitApp:

This directory contains the app.py code which is linked to the Streamlit for deploying the website corresponding to this project. Inside this app, all the visualization functions that are provided in the utils directory are imported first. This app is designed to be as interactive as possible so that users can explore the data more in depth and gain more understanding.
