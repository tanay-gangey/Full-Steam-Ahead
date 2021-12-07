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
        st.subheader('Motivation')

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
        
        st.subheader("Similarity Matrix for User-Playtime Interactions")
        st.write("Thus, this seems to suggest that there might be some similarities in the playtime for certain games for users which play a lot versus those who play less, which is a good place to start for a recommender system. Going along with this, we can start by creating a clustered heatmap of a cosine similarity matrix on this user-game interation data. ")
        
        pairwise_metrics = np.loadtxt("steam-data/baseSimilarity.txt")

        st.pyplot(sns.clustermap(pairwise_metrics))

        st.write("Here, any white square indicates a large region where many users have similar playtimes. Thus, we can see that we have the following:")
        st.write("- Firstly, a large section of users that play similar games on Steam. Looking at this cluster individually, it appears that this cluster is full of those who play games for longer playtimes, focusing on games that can handle that usage, like first-person shooters like CSGO.")
        st.write("- Secondly, we have many smaller clusters, which indicate that we have smaller sub-groups of users with similar behavior. This suggests that a recommender system might do a good job at recommending users games")
        st.write("- Lastly, there's a black band that suggests there's a group that has 0 similarity on all cases, including by itself. As we're using cosine similarity, this suggests that there are several users in the data that have incredibly small recorded playtime or no recorded playtime, despite purchasing games. As these users are hard to understand from play data, it'll be interesting to see how the recommender system does on this data.")
        
        st.subheader("Graph Understanding for User-Playtime Interactions")

        st.write("To understand what's going on a little better, let's try to visualize this heatmap as an undirected graph. Here, two edges are collected if they have a particular cosine similarity, which you can change here:")
        b = st.slider("Threshold for Similarity Score for Graph", min_value=0.4, max_value=0.9, step=0.1)
        #st.write("steam-data/IDS_"+"{:.1f}".format(b)+".png")
        st.image("steam-data/IDS_"+"{:.1f}".format(b)+".png")

        st.write("From this, it can be seen that the cluster of FPS gamers have incredibly high game play-time similarity scores. As cosine similarity is bounded from 0 to 1, having entries with a cosine similarity of 0.9 suggests that there might be games that, if one member recommends, then all others will most definitely like, especially if the member in question plays that game for a long time. Additionally, if you look at putting the threshold at say 0.6, we can easily see that the smaller, but potentially less uniform, communities are still prevalent. From this, we can determine that a recommender system might be useful if it can preserve these similarities, and keep the smaller subgroups. While it would be easy to give the larger subgroup similar recommendations, giving the smaller subgroups similar but different recommendations is also of vital importance, which we can now analyze using this type of analysis.")
        
        
        st.subheader("Recommender System Analysis")
        #@st.cache()
        #/home/arav/CMU/05-839/final/9
        st.title("Low-Rank Approximation")
            
        st.write("The recommender system we are going to look at is the low-rank approximation system, where the user-rating matrix is factored into two low-rank matrices, the product of which is a good fascimile of 'good' recommendations. ")
        st.write("Here, we've plotted the similarity matrices of these lower-rank matrices:")
        
        a = st.slider("Number of Components in LR Approximation", min_value=1, max_value=15, step=1)
        low_rank = np.loadtxt("steam-data/"+str(a)+"ranksimilarity.txt")
        st.pyplot(sns.clustermap(low_rank))
        
        st.write("From here, we can conclude the following about the algorithm:")
        st.write("- For this dataset, a rank one approximation would simply give all users similar recommendations, equal to that of the most prevalent games.")
        st.write("- When we apply a rank two approximation, we are able to approximate two separate 'ranking clusters'. We can immediately see that the group identified before, namely the group with high similarity, is given a recommendation different from the rest of the group, which makes sense as we identified them as a group of people who prefer playing games with multiplayer with high skill depth, like First Person Shooters.")
        st.write("- Applying more and more approximations leads to more and more separate but similar groups of recommendations, which allows us to group together similar recommendations and see that we're not overfitting yet.")
        st.write("- Lastly, even with 15 components, we can see that this algorithm gives many groups of recommendations. However, we can see visually that we're not overfitting, as we haven't replicated the high-diagonal nature of the graph internally. This is incredibly important, as it ensures that our recommendations are going to be novel for the user, which is what we intend")
        
        st.write("Thus, through this data, we can see that a low-rank approximation makes a great recommender system, and we can visually understand why certain settings might fail, as they give too similar recommendations for dissimilar users. ")
