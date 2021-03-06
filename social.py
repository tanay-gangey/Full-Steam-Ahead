import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import pydeck as pdk

import matplotlib.pyplot as plt
import altair as alt
from hydralit import HydraHeadApp
import json
import streamlit.components.v1 as components
import altair as alt
import plotly.express as px

class SocialApp(HydraHeadApp):
    
    def format_month(month):
        if len(month) == 1:
            return "0" + month

    def run(self):
        st.title("Social Impacts of COVID-19: Steam Users")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("In order to understand the impact of a pandemic on the social lifestyles of people, here we are looking at the number of COVID-19 cases acorss the world and the new friends added for a sample of steam users. ")
        
        st.write("\n")
        st.write("Plot 1 shows the total friends added for a sampled user dataset on steam during a month around pandemic")
        st.write("Plot 2 shows the total number of new COVID cases during a month.")
        df = pd.read_csv("steam-data/NewFriends.csv")
        df = df[df['year'] > 2019]
        df['friend_since'] =  pd.to_datetime(df['friend_since'])
        df['year-month'] = df['friend_since'].dt.strftime('%Y/%m')
        df = df.groupby(['year-month']).count().reset_index()
        df2 =df[['user_id' , 'year-month']]
#         df2 = df2.rename(columns={'year-month':'index'}).set_index('index')
#         col1, col2 = st.columns((100, 1))
#         st.line_chart(df2)

        
#         df2 = df2.reset_index().melt('index', var_name='category', value_name='y')

        line_chart = alt.Chart(df2).mark_line(interpolate='basis').encode(
            alt.X('year-month', title='Pandemic Period'),
            alt.Y('user_id', title='New Friends Added'),
        ).properties(
            title='Plot1: Steam Friends Network During Pandemic',
            width=1000,
            height=400
        )

        st.altair_chart(line_chart)

        st.write("\n")
        st.write("\n")
        covid_df = pd.read_csv("covid-data/active_cases.csv")
#         covid_df['ObservationDate'] =  pd.to_datetime(covid_df['ObservationDate'])
#         covid_df['year-month'] = covid_df['ObservationDate'].dt.strftime('%Y/%m')
#         covid_df['Active'] = covid_df['Confirmed'] - covid_df['Recovered'] - covid_df['Deaths']
#         covid_df['Active'] = covid_df['Active']/1000000
#         covid_df = covid_df.groupby('year-month').sum().reset_index()
        
        df2 =covid_df[['Active' , 'year-month']]
#         active_cases = covid_df['Active'].tolist()
#         n = len(active_cases)
#         curr = active_cases[0]
#         for i in range(n-1):
#             temp = active_cases[i+1]
#             active_cases[i+1] = active_cases[i+1] - curr
#             curr = temp
#         covid_df['Active'] = active_cases
        line_chart2 = alt.Chart(df2).mark_line(interpolate='basis').encode(
            alt.X('year-month', title='Pandemic Period'),
            alt.Y('Active', title='New Covid Cases Across the World(in millions)'),
        ).properties(
            title='Plot2: Covid Cases Distribution(Summed over month)',
            width=1000,
            height=400
        )

        st.altair_chart(line_chart2)
        
        st.write("\n")
        st.write("We observed that during the early days of pandemic there was a sudden rise in the new friends added on steam. As the number of COVID cases rose, serveral countries had imposed complete lockdowns which led to a sudden fall in the social lives of people. Clearly, people needed some source of social interaction because of which a large number of people got into online multiplayer gaming.")
        
        
    