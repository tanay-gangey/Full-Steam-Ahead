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

        px_bar = px.bar(top_20_percent,
                        x='country', y='achievement',
                        title='Distribution Of Players (top 20%) Across Countries',
                        color='appname',
                        labels={"country": "Countries"})
        st.plotly_chart(px_bar, use_container_width=True)

        scatter_chart = st.altair_chart(
            alt.Chart(top_10_playtime_vs_achievement)
            .mark_circle(size=60)
            .encode(x='total_playtime', y='achievement', color='appname', tooltip=['appname', 'steamid'])
            .interactive(), use_container_width=True
        )

        combined_country_wise_player = pd.read_csv(
            "steam-data/country_wise_player_time.csv")

        country_wise_time = combined_country_wise_player.groupby(["country", "lat", "lon"])[
            ["total_playtime"]].agg("sum").reset_index()

        with open('steam-data/customgeo.json') as f:
            countries = json.load(f)

        fig = px.choropleth(country_wise_time, geojson=countries, locations="country",
                            featureidkey="properties.iso_a2",
                            color='total_playtime',
                            labels={"country": "Country"},
                            hover_data=["country", "total_playtime"])
        st.plotly_chart(fig, use_container_width=True)
