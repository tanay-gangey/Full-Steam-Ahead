import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
from sklearn.decomposition import NMF

from hydralit import HydraHeadApp

#create a wrapper class
class AdvancedApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        st.title('Analysis of the Low-Rank Approximation for Recommending User Playtimes')
        st.info('TODO')

        st.write("One of the most interesting applications of steam user information is in recommender systems, where we can try to recommend games that people might like to individuals who haven't played them. Given the playtime metrics, let's develop a simple recommender system for these metrics and see how it groups users together, as similar users should be grouped together.")
        st.write("To this end, let's first load in the Games.csv file and start by visualizing the overall distribution of game playtimes.")

        st.image("steam-data/1DUserPlot.png", caption="Distribution of Playtime Across Individual Games and Users, in Hours.")


        st.write("From the graph, we can immediately see the following:")
        st.write("- Firstly, the left half of the graph demonstrates that Steam users will test the game for some time ( usually less than 1 hour ), to see if they like it and will continue playing.")
        st.write("- If they do, evidenced by still playing after an hour, then they'll continue to play till about 10 hours into the game.")
        st.write("- However, past that point, the trend is exponentially decreasing. Playing 100 hours is possible, but relatively rare, while only really few play 1000 hours of a game.")
        
        st.write("We can also look at different total playtimes per user, and get the following relationship: ")
        
        st.image("steam-data/1DUserDist.png", caption="Distribution of Playtime Among Users, in Hours.")
        
        st.write("Here, we see that there's an approximately exponential distribution among users who play on Steam, with the users that play more being less frequent than users that play less.")
        
        st.write("Thus, this seems to suggest that there might be some similarities in the playtime for certain games for users which play a lot versus those who play less, which is a good place to start for a recommender system. Going along with this, we can ")
        
        pairwise_metrics = np.loadtxt("steam-data/baseSimilarity.txt")





        b = st.slider("Threshold for Similarity Score for Graph", min_value=0.4, max_value=0.9, step=0.1)
        #st.write("steam-data/IDS_"+"{:.1f}".format(b)+".png")
        st.image("steam-data/IDS_"+"{:.1f}".format(b)+".png")

        #@st.cache()
        #/home/arav/CMU/05-839/final/9
        st.title("Low-Rank Approximation")
            
            
        a = st.slider("Number of Components in LR Approximation", min_value=1, max_value=15, step=1)
        low_rank = np.loadtxt("steam-data/"+str(a)+"ranksimilarity.txt")
        st.pyplot(sns.clustermap(low_rank))
