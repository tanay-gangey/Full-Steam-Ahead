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

        df_sampled = df

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

        top_country_players = df_sampled[["country", "percentage_players"]].drop_duplicates(
        ).nlargest(20, 'percentage_players')

        px_bar = px.bar(top_country_players, x='country', y='percentage_players',
                        title='Percentage Distribution Of Players Across Top 20 Countries', labels={"percentage_players": "% of Total Players in sample", "country": "Countries"})
        st.plotly_chart(px_bar, use_container_width=True)

        df_friends = pd.read_csv(
            'steam-data/merged_data_friends_with_loc.csv')

        metrics = []
        for country in top_country_players['country']:
            country_relation_info = df_friends[["country_a", "country_b"]]
            country_relation_info = country_relation_info[
                (country_relation_info["country_a"] == country) | (country_relation_info["country_b"] == country)]

            same_count = country_relation_info[country_relation_info[
                'country_a'] == country_relation_info['country_b']].shape[0]

            diff_count = country_relation_info[country_relation_info[
                'country_a'] != country_relation_info['country_b']].shape[0]

            tc = same_count + diff_count
            same_count = same_count / tc
            diff_count = diff_count / tc
            metrics.append({
                "country": country,
                "same_count": same_count,
                "diff_count": diff_count
            })
        metrics = pd.read_json(json.dumps(metrics))

        px_bar = px.bar(metrics, x='country', y=['same_count', 'diff_count'],
                        title='Percentage Distribution Of Friendships Within Same Countries Or Different Countries',
                        labels={"same_count": "Friendships within same countries",
                                "diff_count": "Friendships in different countries",
                                "country": "Countries", "value": "Percentage"}, barmode='group')
        st.plotly_chart(px_bar, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            selector_a = df_friends['country_a'].unique()
            selector_a = selector_a[selector_a != "US"]
            selector_a = np.insert(selector_a, 0, "US")
            country_selectbox_a = st.selectbox(
                "Select Country A",
                tuple(selector_a)
            )

        with col2:
            selector_b = df_friends['country_b'].unique()
            selector_b = selector_b[selector_b != "IN"]
            selector_b = np.insert(selector_b, 0, "IN")
            country_selectbox_b = st.selectbox(
                "Select Country B",
                tuple(selector_b)
            )

        filtered_df = df_friends[df_friends[
            'country_a'] == country_selectbox_a]
        filtered_df = filtered_df[filtered_df[
            'country_b'] == country_selectbox_b]

        filtered_df['tilt'] = np.random.randint(-25, 25, filtered_df.shape[0])

        scatterplot_1 = pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            radius_scale=20,
            get_position=["lon_a", "lat_a"],
            get_fill_color=[0, 0, 0],
            get_radius=2000,
            pickable=True,
        )

        scatterplot_2 = pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            radius_scale=20,
            get_position=["lon_b", "lat_b"],
            get_fill_color=[0, 0, 0],
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
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=35.99934160945984,
                longitude=-32.11052813375463,
                zoom=1,
                # pitch=50,
            ),
            layers=layers,
            tooltip={
                "html": "<b>User 1:</b> {lon_a}, {lat_a}, {country_a} <br/> <b>User 2:</b> {lon_b}, {lat_b}, {country_b}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }

        ))
