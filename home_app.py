import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hydralit import HydraHeadApp
import seaborn as sns
import plotly.express as px
import pydeck as pdk

import matplotlib.pyplot as plt
import altair as alt
from hydralit import HydraHeadApp
import json
import streamlit.components.v1 as components

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import streamlit as st
import plotly.figure_factory as ff


#create a wrapper class
class HomeApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        st.title('Full Steam Ahead!')
        st.write('''
        Our goal with this project is to understand the users of the biggest PC game distribution platform of the world, **Steam**, both in terms of users and games. 
        While Steam is traditionally seen as a  distribution platform, it also acts as a social network. Players can connect with others for multiplayer gaming sessions, chatting and comparing their in-game statistics. 
        
        While a lot of work have already been done on social network analysis for platforms like Twitter, Facebook and Instagram, similar studies haven't been done as extensively for Steam. Through our analysis, we want to understand what makes Steam, and the people who use it, interesting.
        We try to answer the following questions:
        - Where do Steam users come from?
        - How do Steam users interact across the globe?
        - How did the COVID-19 pandemic change the interactions and connections of these users?
        - Can we use our data to generate recommendations for Steam users, and understand it in terms of the communities formed by similar playtime?
        ''')

        st.write("---")

        st.subheader('Around the World')

        st.write("""
            In order to visualize Steam usage around the world, we sample a dataset of 100,000 Steam users and plot their locations on an interactive world map. One can also view country-wise distribution by using the drop-down on top of the world map to apply a country filter.
        """)
        df = pd.read_csv(
            'steam-data/loc_lat_lng_data_100kUsers.csv')

        st.write("""
            We can see that Steam as a gaming platform is quite popular around the globe.
        """)

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

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=35.99934160945984,
                longitude=-32.11052813375463,
                zoom=1,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=filtered_df,
                    radius_scale=20,
                    get_position=["lon", "lat"],
                    get_fill_color=[220, 20, 60],
                    get_radius=2000,
                    pickable=True,
                )
            ],
            tooltip={
                "html": "<b>Location:</b> {lon}, {lat}, {country}",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }

        ))
        # st.map(filtered_df, zoom=1)

        top_country_players = df_sampled[["country", "percentage_players"]].drop_duplicates(
        ).nlargest(20, 'percentage_players')

        st.write(""" 
            Next we want to see which countries have the most number of players. Below we have given a bar graph displaying the top 20 countries with the highest percentage of players. From the bar graph we see that countries such as USA, Russia, Germany, Brazil & Great-Britain have the highest number of users.
        """)

        px_bar = px.bar(top_country_players, x='country', y='percentage_players',
                        title='Percentage Distribution Of Players Across Top 20 Countries', labels={"percentage_players": "% of Total Players in sample", "country": "Countries"})
        st.plotly_chart(px_bar, use_container_width=True)

        st.write(""" 
            We also wanted to explore the locational distribution of Steam connections and whether there are a large number of users who are connected across regions. We intend to see if this might indicate that the communities formed are more collaborative and interesting to study compared to traditional social networks which tend to follow people who live near each other. This helps us see how gaming is bringing the world together.
        """)

        st.write(""" 
            We have first plotted for the top 20 countries, the percentage of Friendships users have within their own country compared to the percentage of friendships that users have outside their country. We see a general trend of users having larger number of friends outside their own country. This supports our belief that in contrast to regular Social Media, Gaming is indeed helping people make connections around the world.
        """)

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
                "Friendships Within Same Country": same_count,
                "Friendships Within Different Country": diff_count
            })
        metrics = pd.read_json(json.dumps(metrics))

        px_bar = px.bar(metrics, x='country', y=['Friendships Within Same Country', 'Friendships Within Different Country'],
                        title='Percentage Distribution Of Friendships Within Same Countries Or Different Countries',
                        labels={"country": "Countries", "value": "Percentage"}, barmode='group')

        # texts = ["Friendships within same countries",
        #          "Friendships in different countries"]
        # for i, t in enumerate(texts):
        #     px_bar.data[i].text = t
        #     px_bar.data[i].textposition = 'outside'

        st.plotly_chart(px_bar, use_container_width=True)

        st.write(""" 
            #####  Here we have an interactive graph where we can visualize the number of Friendships between Steam users of any two countries within our sample.
        """)

        st.write(""" 
            Please select Country A and Country B from the dropdowns to view the number of connections between these two countries.
        """)

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
        ##########################
        st.write("---")

        st.subheader('Top Players')

        st.write("""
            In this section we wanted to explore the characterstics of top players across the globe. Our first mission was to find what makes a top player. Our analysis led us to the conclusion that among all the other features the total playtime of a user is the primary determining factor and has a very high correlation with the number of achievements a player holds.
        """)

        st.write("""
            Given below is a scatter plot to show the high correlation.
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

        top_5_games = top_20_percent['appid'].value_counts().head(5).reset_index()['index'].tolist()
        top_20_percent.loc[~top_20_percent['appid'].isin(top_5_games), 'appname'] = 'Other'

        scatter_chart = st.altair_chart(
            alt.Chart(top_10_playtime_vs_achievement)
            .mark_circle(size=60)
            .encode(x=alt.X('total_playtime', title="Total Playtime"), y=alt.Y('achievement', title='Number Of Achievements'), color=alt.Color('appname', title='Games'), tooltip=['appname', 'steamid'])
            .interactive(), use_container_width=True
        )
        st.write("""
            Next we wanted to see which countries have the most number of top players. To visualize this we have a graph here to show the number of achievements of players in the top 20 countries.
        """)
        st.write("""
            Russia seems to produce the most number of top players followed by United States
        """)

        px_bar = px.histogram(top_20_percent,
                        x='country', y='achievement',
                        title='Distribution Of Players (top 20%) Across Countries',
                        # color='appname',
                        labels={"country": "Countries", "achievement": "Number of Achievements"})
        px_bar.update_layout(yaxis_title="Number of Achievements")

        st.plotly_chart(px_bar, use_container_width=True)

        combined_country_wise_player = pd.read_csv(
            "steam-data/country_wise_player_time.csv")

        st.write("""
            Given below we also have an interactive map which shows the total playtime across the top 20 countries. This also supports our analysis that the total playtime is the main contributing factor to making a Top Player. Russia, which produces the maximum number of Top Players has one of the highest total play-times as a country.
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
        ###################################

        st.write("""---""")
        st.subheader("Social Impacts of COVID-19: Steam Users")
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
        df2 = df2[:-7]
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
        
        df3 =covid_df[['Active' , 'year-month']]
#         active_cases = covid_df['Active'].tolist()
#         n = len(active_cases)
#         curr = active_cases[0]
#         for i in range(n-1):
#             temp = active_cases[i+1]
#             active_cases[i+1] = active_cases[i+1] - curr
#             curr = temp
#         covid_df['Active'] = active_cases
        line_chart2 = alt.Chart(df3).mark_line(interpolate='basis').encode(
            alt.X('year-month', title='Pandemic Period'),
            alt.Y('Active', title='New Covid Cases Across the World(in millions)'),
        ).properties(
            title='Plot2: Covid Cases Distribution(Summed over month)',
            width=1000,
            height=400
        )

        st.altair_chart(line_chart2)
        
        fig1 = go.Scatter(
            x=df2["year-month"],
            y=df2["user_id"],
            name="New Friends Added During the Month"
            
        )
        fig2 = go.Scatter(
            x=df3["year-month"],
            y=df3["Active"],
            name='New COVID-19 Cases(in millions)',
            yaxis='y2'
        )
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(fig1)
        fig.add_trace(fig2, secondary_y=True)
        fig['layout'].update(height=600, width=1200,
                         font_color="black",
                         template='seaborn',
                         plot_bgcolor="rgba(255, 255, 255, 255)"
                         )
        st.plotly_chart(fig)


        st.write("\n")
        st.write("We observed that during the early days of pandemic there was a sudden rise in the new friends added on steam. As the number of COVID cases rose, serveral countries had imposed complete lockdowns which led to a sudden fall in the social lives of people. Clearly, people needed some source of social interaction because of which a large number of people got into online multiplayer gaming.")
        
        st.write("From the time series, we can see that the there is a great increase in friends at the start of the pandemic, the rate of which decreases later on, but tends to go with the COVID 19 movement. This makes sense, as it is hypothesized that a lot of people started to play more video games as the pandemic went on. To better understand this trend, we visualized a 100,000 user subset among the user data we had as a dynamic graph below, which is an animation of the new friendships over the course of the pandemic. From here, we can see the explosion of new friendships as the pandemic starts, along with the general increase in social clustering that social networks create.")
        st.image("steam-data/dynamic.gif")

        st.write("---")    
    