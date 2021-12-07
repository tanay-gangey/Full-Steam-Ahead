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


class TopPlayersVizApp(HydraHeadApp):

    def run(self):
        st.write("""
            ##### In this section we wanted to explore the characterstics of top players across the globe. Our first mission was to find what makes a top player. Our analysis led us to the conclusion that among all the other features the total playtime of a user is the primary determining factor and has a very high correlation with the number of achievements a player holds.
        """)

        st.write("""
            ##### Given below is a scatter plot to show the high correlation.
        """)

        combined_achievement_data = pd.read_csv(
            "steam-data/combined_achievement_data.csv")
        loc_df = pd.read_csv(
            'steam-data/loc_lat_lng_data_100kUsers.csv')

        playtime_vs_achievement = combined_achievement_data.groupby(
            ["appid", "appname", "steamid", "total_playtime"]).agg({"achievement": "count"}).reset_index()

        top_10_apps = playtime_vs_achievement[
            'appid'].value_counts().nlargest(10)

        top_10_playtime_vs_achievement = playtime_vs_achievement[
            playtime_vs_achievement['appid'].isin(top_10_apps.index)]

        top_country_achievement = playtime_vs_achievement.merge(loc_df, on="steamid").dropna(
        )[["appid", "appname", "steamid", "total_playtime", "achievement", "country"]]

        quantile_80 = top_country_achievement.achievement.quantile(0.8)

        top_20_percent = top_country_achievement[
            top_country_achievement['achievement'] > quantile_80]

        scatter_chart = st.altair_chart(
            alt.Chart(top_10_playtime_vs_achievement)
            .mark_circle(size=60)
            .encode(x=alt.X('total_playtime', title="Total Playtime"), y=alt.Y('achievement', title='Number Of Achievements'), color=alt.Color('appname', title='Games'), tooltip=['appname', 'steamid'])
            .interactive(), use_container_width=True
        )

        st.write("""---""")

        st.write("""
            ##### Next we wanted to see which countries have the most number of top players. To visualize this we have a graph here to show the number of achievements of players in the top 20 countries.
        """)
        st.write("""
            ##### Russia seems to produce the most number of top players followed by United States
        """)

        px_bar = px.bar(top_20_percent,
                        x='country', y='achievement',
                        title='Distribution Of Players (top 20%) Across Countries',
                        color='appname',
                        labels={"country": "Countries", "achievement": "Number of Achievements"})
        st.plotly_chart(px_bar, use_container_width=True)

        combined_country_wise_player = pd.read_csv(
            "steam-data/country_wise_player_time.csv")

        st.write("""
            ##### Given below we also have an interactive map which shows the total playtime across the top 20 countries.
        """)

        country_wise_time = combined_country_wise_player.groupby(["country", "lat", "lon"])[
            ["total_playtime"]].agg("sum").reset_index()

        with open('steam-data/customgeo.json') as f:
            countries = json.load(f)

        fig = px.choropleth(country_wise_time, geojson=countries, locations="country",
                            featureidkey="properties.iso_a2",
                            color='total_playtime',
                            title="Total Playtime Across Top 20 Countries",
                            labels={"country": "Country"},
                            hover_data=["country", "total_playtime"])
        st.plotly_chart(fig, use_container_width=True)
