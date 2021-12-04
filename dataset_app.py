import streamlit as st
import numpy as np
import pandas as pd

from hydralit import HydraHeadApp

#create a wrapper class
class DatasetApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        st.markdown("<h1 style='text-align: center;'>About the Data</h1>", unsafe_allow_html=True)
        st.header("Datasets and Motivation")
        st.subheader("\tSteam Dataset")
        steamintro = """\tSteam is a video game digital distribution system that provides the user 
        with community features such as friends lists and groups and cloud storage.
        We obtained data about various aspects of the platforms such as the friend network, 
        the achievement completion of each game, the number of hours of games that each user has played 
        during their time on the platform. We used two different sources to obtain this data. First, we
        used the dataset collected by BYU for the 2016 ACM Internet Measurement Conference. To augment 
        this data, we used the Steam Web API to collect more recent data. The API allowed us to collect
        extensive information about the games and users on Steam. 
        
            """
        st.write(steamintro)
        st.subheader("\tCovid-19 Dataset")
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
        #TODO
        st.info("Insert table here w/ summary of data like here: https://yelpcmu.weebly.com/dataset.html")
        
        st.markdown('''
                    ---
                    ''')
                    
        col1, col2 = st.columns(2) 
        
        with col1:
            st.header("Completeness")
            st.write("About the completeness")
        with col2:
            st.header("Coherence")
            st.write("About coherence")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.header("Correctness")
            st.write("About the correctness")
        with col4:
            st.header("Accountability")
            st.write("About accountability")
        
        st.markdown('''
                    ---
                    ''')
                    
        st.header("Data Processing")
        st.write("About what cleaning we did, maybe a before/after type sitch, oh and ofc the sql->csv process")
        
        st.markdown('''
                    ---
                    ''')
        
        st.header("Dataset Statistics")
        st.write("Pairs of line and then interactive graph explaining the dataset")
        
        st.markdown('''
                    ---
                    ''')
        
        st.subheader("Sources")
        st.write("[1] https://steam.internet.byu.edu/")
        st.write("[2] https://developer.valvesoftware.com/wiki/Steam_Web_API")
        st.write("[3] https://www.kaggle.com/imdevskp/corona-virus-report")

                    