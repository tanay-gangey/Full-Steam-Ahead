import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import datetime
import plotly.express as px
from hydralit import HydraHeadApp

# create a wrapper class
class CovidDatasetApp(HydraHeadApp):

    # wrap all your code in this method and you should be done
    #def run(self):
        all_covid_data = pd.read_csv("covid-data/full_grouped.csv")
        county_covid_data = pd.read_csv("covid-data/usa_county_wise.csv")

        st.header("\tCovid-19 Dataset")
        covidintro = """\tFor the past two years, people around the world have been affected by the
        global COVID-19 pandemic. This has led to a reduction in outdoor activities and inspired people
        to find alternate sources of entertainment. We hypothesize that the Steam platform and gaming 
        community has been an important source of catharsis for many people affected around the globe. 
        We analyse the effect the pandemic has had in terms of the growth of the community, the time 
        spent on the Steam platform and the achievement completion percentage of games on the platform.
        We collected the COVID-19 data from Kaggle. The dataset contains information about the daily cases
        in each country in the world as well as the county-wise data for the United States. 
            """
        st.write(covidintro)
        with st.expander("FULL_GROUPED.CSV"):
            st.write('''
            * Date: Date corresponding to the data for each row
            * Country/Region: Country corresponding to the COVID-19 data 
            * Confirmed: The cumulative number of confirmed cases 
            * Deaths: The cumulative number of deaths
            * Recovered: Total number of recoveries in the country of interest
            * Active: Total number of active cases in the country of interest
            * New cases: New cases reported on this date
            * New deaths: New deaths reported on this date
            * New recovered: New recoveries reported on this date
            * WHO Region: Broad region as classified by WHO
            ''')
            st.write('\n')
            st.write('Sample:')
            st.dataframe(all_covid_data.sample(n=5).reset_index(drop=True))
    

        with st.expander("USA_COUNTY_WISE.CSV"):
            st.write('''
            * Date: Date corresponding to the data for each row
            * Combined_Key: A string thta contains the admin, state and country 
            * Lat: Latitude corresponding to the combined key 
            * Long_: Longitude corresponding to the combined key
            * Deaths: The cumulative number of deaths
            * Confirmed: Total number of confirmed cases in the county of interest
            ''')
            st.write('\n')
            st.write('Sample:')
            st.dataframe(county_covid_data.sample(n=5).reset_index(drop=True))
            
        #################################################################################################################

        st.subheader('Temporal Exploration')
        st.write('Let\'s start by looking how people were affected with time during the pandemic.')
        countries = tuple(all_covid_data["Country/Region"].unique())
        selectedcountry = st.selectbox(
            "Choose your country of interest", countries)

        columns = ("Confirmed", "Deaths", "Recovered", "Active")
        datatype = st.radio(
            "What type of data do you want to see?", ('Cumulative', 'Daily'))
        if(datatype == "Daily"):
            columns = ("New cases", "New deaths", "New recovered")
        option = st.selectbox("Choose metric to plot", columns)

        plotdf = all_covid_data[all_covid_data["Country/Region"]
                                == selectedcountry]
        fig = px.line(plotdf,x="Date",y=option)
        
        st.plotly_chart(fig, use_container_width=True)

        #################################################################################################################
        
        st.subheader('Regional Exploration')
        st.write('We can also see the distribution of active cases at different times across the different counties in the United States.')
        county_covid_data["Date"] = pd.to_datetime(
                county_covid_data["Date"])
        county_covid_data["Date"] = county_covid_data["Date"].dt.strftime(
            '%Y-%m-%d')
        datesel = st.date_input(
            "Enter a date between 22-Jan 2020 and 27-Jul-2020", datetime.date(2020, 6, 15))
        dailydata = county_covid_data[county_covid_data['Date'] == str(
            datesel)]
        dailydata_clean = dailydata[["Date", "Lat", "Long_", "Confirmed", "Combined_Key"]]
        dailydata_clean.columns = ["Date", "lat", "lon", "confirmed", "County"]
        midpoint = (np.average(dailydata_clean["lat"]), np.average(
            dailydata_clean["lon"]))

        def map(data, lat, lon, zoom):
            data['normalized'] = (data['confirmed'] - data['confirmed'].min()) / (
                data['confirmed'].max() - data['confirmed'].min())

            st.write(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": lat,
                    "longitude": lon,
                    "zoom": zoom,
                    "pitch": 50,
                },
                layers=[
                    pdk.Layer(
                        "ColumnLayer",
                        data=data,
                        get_position=["lon", "lat"],
                        get_elevation="confirmed",
                        elevation_scale=40,
                        radius=5000,
                        get_fill_color=[0, 128, 255, 255],
                        pickable=True,
                        auto_highlight=True,
                    ),
                ],
                tooltip={
                    'html': '<b>Active cases:</b> {confirmed}<br><b>County:</b> {County}',
                    'style': {
                        'color': 'white'
                    }
                }
            ))

        map(dailydata_clean, midpoint[0], midpoint[1], 3)
    