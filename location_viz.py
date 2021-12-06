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

        st.map(filtered_df, zoom=1)

        df_friends = pd.read_csv(
            'steam-data/merged_data_friends_with_loc.csv')  # .sample(frac=sample_slider)

        col1, col2 = st.columns(2)
        with col1:
            country_selectbox_a = st.selectbox(
                "Select Country A",
                tuple(df_friends['country_a'].unique())
            )

        with col2:
            country_selectbox_b = st.selectbox(
                "Select Country B",
                tuple(df_friends['country_b'].unique())
            )

        filtered_df = df_friends[df_friends[
            'country_a'] == country_selectbox_a]
        filtered_df = filtered_df[filtered_df[
            'country_b'] == country_selectbox_b]

        filtered_df['tilt'] = np.random.randint(-50, 50, filtered_df.shape[0])

        scatterplot_1 = pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            radius_scale=20,
            get_position=["lon_a", "lat_a"],
            get_fill_color=[0, 255, 0],
            get_radius=2000,
            pickable=True,
        )

        scatterplot_2 = pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            radius_scale=20,
            get_position=["lon_b", "lat_b"],
            get_fill_color=[0, 255, 0],
            get_radius=2000,
            pickable=True,
        )

        line_layer = pdk.Layer(
            "ArcLayer",
            data=filtered_df,
            get_source_position=["lon_a", "lat_a"],
            get_target_position=["lon_b", "lat_b"],
            get_source_color=[255, 140, 0],
            get_target_color=[255, 140, 0],
            get_width=2,
            get_tilt=["tilt"],
            highlight_color=[255, 255, 0],
            picking_radius=1000,
            auto_highlight=True,
            pickable=True,
        )

        layers = [scatterplot_1, scatterplot_2, line_layer]

        st.pydeck_chart(pdk.Deck(
            # map_style='mapbox://styles/mapbox/light-v9',
            layers=layers,
            tooltip={
                "html": "<b>User 1:</b> {lon_a}, {lat_a}, {country_a} <br/> <b>User 2:</b> {lon_b}, {lat_b}, {country_b}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }

        ))

        # r = pdk.Deck(
        #     layers=layers,
        #     tooltip={
        #         "html": "<b>User 1:</b> {lon_a}, {lat_a}, {country_a} <br/> <b>User 2:</b> {lon_b}, {lat_b}, {country_b}",
        #         "style": {
        #             "backgroundColor": "steelblue",
        #             "color": "white"
        #         }
        #     }

        # )

        # r.to_html("out.html")

        # with open("out.html") as f:
        #     components.html(f.read())
