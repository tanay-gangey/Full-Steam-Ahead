import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import pydeck as pdk

import matplotlib.pyplot as plt
import altair as alt
from hydralit import HydraHeadApp
import json


class LocationVizApp(HydraHeadApp):

    def run(self):
        df = pd.read_csv(
            'steam-data/loc_lat_lng_data_100kUsers.csv')

        df_sampled = df  # .sample(10000)

        countries = ["All"] + df['country'].unique().tolist()
        country_selectbox = st.selectbox(
            "Select Country",
            tuple(countries)
        )

        if (country_selectbox != "All"):
            filtered_df = df_sampled[df_sampled[
                'country'] == country_selectbox]
        else:
            filtered_df = df_sampled

        # with open('./steam-data/customgeo.json') as f:
        #     countries = json.load(f)
        # st.write("hello")

        st.map(filtered_df, zoom=1)
