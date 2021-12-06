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

class SocialApp(HydraHeadApp):
    
    def format_month(month):
        if len(month) == 1:
            return "0" + month

    def run(self):
        df = pd.read_csv("steam-data/NewFriends.csv")
        df = df[df['year'] > 2019]
        df['friend_since'] =  pd.to_datetime(df['friend_since'])
        df['year-month'] = df['friend_since'].dt.strftime('%Y/%m')
        df = df.groupby(['year-month']).count().reset_index()
        df2 =df[['user_id' , 'year-month']]
        df2 = df2.rename(columns={'year-month':'index', 'user_id':'friends_count'}).set_index('index')
        st.line_chart(df2)
        
        
        covid_df = pd.read_csv("covid-data/covid_19_data.csv")
        covid_df['ObservationDate'] =  pd.to_datetime(covid_df['ObservationDate'])
        covid_df['year-month'] = covid_df['ObservationDate'].dt.strftime('%Y/%m')
        covid_df['Active'] = covid_df['Confirmed'] - covid_df['Recovered'] - covid_df['Deaths']
        covid_df['Active'] = covid_df['Active']/1000000
        covid_df = covid_df.groupby('year-month').sum().reset_index()
        
        df2 =covid_df[['Active' , 'year-month']]
        df2 = df2.rename(columns={'year-month':'index'}).set_index('index')
        st.line_chart(df2)
        
    