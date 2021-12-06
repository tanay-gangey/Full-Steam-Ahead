import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from hydralit import HydraHeadApp

#create a wrapper class
class SteamDatasetApp(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):
        achievement_pct = pd.read_csv("steam-data/Achievement_Percentages.csv")
        achievement_pct.columns = ['index', 'appid', 'name', 'percentage']
        achievement_pct = achievement_pct.drop(['index'],axis=1)

        app_ids_info = pd.read_csv("steam-data/App_ID_Info.csv")
        app_ids_info.columns = ['index', 'appid', 'Title', 'Type', 'Price', 'Release_Date', 'Rating', 'Required_Age', 'Is_Multiplayer']
        app_ids_info = app_ids_info.drop(['index'],axis=1)

        games_genres = pd.read_csv('steam-data/Games_Genres.csv', header=None)
        games_genres.columns = ['index', 'appid', 'Genre']
        games_genres = games_genres.drop(columns = ['index'])

        game_publishers = pd.read_csv("steam-data/Games_Publishers.csv", header=None)
        game_publishers.columns = ['index', 'appId', 'publisher']
        game_publishers = game_publishers.drop(columns = ['index'])

        game_developers = pd.read_csv("steam-data/Games_Developers.csv", header=None)
        game_developers.columns = ['index', 'appId', 'developer']
        game_developers = game_developers.drop(columns = ['index'])

        user_games = pd.read_csv("steam-data/Games.csv")
        user_games.columns = ['index', 'appid', 'playtime_forever', 'playtime_windows_forever', 'playtime_mac_forever', 'playtime_linux_forever', 'steamid', 'playtime_2weeks']
        user_games = user_games.drop(columns = ['index'])

        # # Friends Information
        # friends = pd.read_csv("steam-data/Friends.csv", header=None, nrows=1000000)
        # friends.rename(columns = {1:'steamId1', 2:'steamId2', 3: "relationship", 4: "friends_since", 5: "timestamp"},inplace = True)
        # friends.drop(0,axis=1, inplace=True)

        #  idx, appid, title, type, Price, Release_date, Rating, Required_Age, Is_Multiplayer

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
        st.markdown('''
        In order to collect and work on the data via pandas and other libraries we converted the data from the SQL dump available at the source to a CSV format. This was done in two steps:    
        - First we used mysqldump to import the SQL data into a MySQL db.
        - Then using a python script we extracted and converted the data into multiple CSV files.
        - It is worth noting that the entire data was over 170GB in size and we are using a subset of that data.

        Given below is the description of all the data in our dataset along with the description of the columns in each CSV file.
        ''')
        with st.expander("ACHIEVEMENT_PERCENTAGES.CSV"):
            st.write("""
        * appid : The ID of the game in question
        * Name : The name of the achievement as it appears to players. As an internal value assigned by developers, its descriptiveness of the achievement varies.
        * Percentage : The percentage of players who have finished this achievement out of all total players who own this game.
            """)
            st.write('\n')
            st.dataframe(achievement_pct.sample(n=5).reset_index(drop=True))

        with st.expander("APP_ID_INFO.CSV"):
            st.write("""
        * appid : The ID of the "app" in question, which is not necessarily a game.
        * Title : The Title of the app, as it appears to users
        * Type : The type of the "app". Possible values include: "demo," "dlc," "game," "hardware," "mod," and "video." Game is the most common.
        * Price : The current price of the "app" on the Steam storefront, in US dollars. Free items have a price of 0.
        * Release_Date : The date the "app" was made available via the Steam storefront. Note that apps released elsewhere originally and later published through steam carry the date of the Steam publish
        * Rating : The rating of the "app" on Metacritic. Set to -1 if not applicable.
        * Required_Age : The MSRB or PEGI-assigned age requirement for viewing this game in the Steam storefront, and, by extension, clicking the button to purchase it.
        * Is_Multiplayer : A value of either 0 or 1 indicating whether or not an "app" contains multiplayer content. Self-reported by developers.
            """)
            st.write('\n')
            st.dataframe(app_ids_info.sample(n=5).reset_index(drop=True))

        with st.expander("FRIENDS.CSV"):        
            st.write("""
        * steamid_a : The Steam ID of the user who's friend list was queried
        * steamid_b : The Steam ID of the a user who is a friend of the user referenced by steamid_a
        * relationship : The type of relationship represented by this entry. Currently the only value used is "friend"
        * friend_since : The date and time when the users in this entry became friends. Note that this field was added in 2009 and thus all frienships existing previous this date are recorded with the default unix timestamp (1970)
        * dateretrieved : Timestamp when this friend list data was requested from the API
            """)

        with st.expander("GAMES_DEVELOPERS.CSV"):        
            st.write('''
        * appid : ID of the app in question
        * Developer : A developer of the app in question. Note that some apps have multiple developers and thus numerous distinct rows with the same appid are possible.
            ''')
            st.write('\n')
            st.dataframe(game_developers.sample(n=5).reset_index(drop=True))

        with st.expander("GAMES_GENRES.CSV"):
            st.write('''
        * appid : ID of the app in question
        * Genre : A genre of the app in question. Note that most apps have multiple genres and thus numerous distinct rows with the same appid are possible.
            ''')
            st.write('\n')
            st.dataframe(games_genres.sample(n=5).reset_index(drop=True))

        with st.expander("GAMES.CSV"):
            st.write('''
        * steamid : The steam ID of the user in question
        * appid : The ID of a given app in the user's library
        * playtime_2weeks : The total time the user has run this app in the two-week period leading up to when this data was requested from the API. Values are given in minutes.
        * playtime_forever : The total time the user has run this app since adding it to their library. Values are given in minutes.
        * playtime_windows_forever : The total time the user has run this app on windows.
        * playtime_mac_forever : The total time the user has run this app on mac.
        * playtime_linux_forever : The total time the user has run this app on linux.
            ''')
            st.write('\n')
            st.dataframe(user_games.sample(n=5).reset_index(drop=True))

        with st.expander("PLAYER_SUMMARIES.CSV"):
            st.write('''
        * steamid : The Steam ID of the user in question
        * lastlogoff : Timestamp of the time when this game data was requested from the API
        * primaryclanid : The groupid (Groups::groupid) of the group that the user has designated as their primary group
        * timecreated : Timestamp of the time when the account was created
        * gameid : If the user was in-game at the time of the API request, this value specifies which game they were running at the time
        * gameserverip : If the user was in-game at the time of the request, and playing a game using Steam matchmaking, this value specifies the IP of the server they were connected to. Is otherwise set to "0.0.0.0:0"
        * loccountrycode : ISO-3166 code for the country in which the user resides. Self-reported.
        * locstatecode : State where the user resides. Self-reported.
        * loccityid : Internal Steam ID corresponding to the city where the user resides. Self-reported.
        * dateretrieved : Timestamp of the time when this game data was requested from the API
            ''')

        st.markdown('''
                    ---
                    ''')

        #################################################################################################################

        st.subheader('Exploring Achievements')

        st.write('''
        Steam Stats and Achievements provides an easy way for your game to provide persistent, roaming achievement and statistics tracking for your users. The user's data is associated with their Steam account, and each user's achievements and statistics can be formatted and displayed in their Steam Community Profile. \n
        In addition to providing highly-valued rewards to players of your games, achievements are useful for encouraging and rewarding teamwork and player interaction, providing extra dimensionality to the game objectives, and rewarding users for spending more of their time in-game.
        ''')

        st.write('''
        We'll first try to see whether people actually care about unlocking achievements or not by looking at the distribution of the achievement completion percentage across games.
        ''')
        joined_data = achievement_pct.merge(app_ids_info, left_on="appid", right_on="appid", how="inner")
        hist_data = joined_data['percentage'].sample(n=2000)
        st.plotly_chart(px.histogram(hist_data, title='Achievement Completion Percentage Distribution'))

        # fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1], show_hist=False, curve_type="kde")
        # st.plotly_chart(fig, use_container_width=True)

        st.write('''
        Next we'll see the Top 10 Most and Least completed games in term of achievements.
        ''')

        joined_data["Joined"] = joined_data["appid"].astype(str) + " "+joined_data["name"].astype(str)
        stat = joined_data[["Title","percentage"]].groupby("Title",as_index=False).agg(mean=('percentage','mean'),count=('percentage','count')).sort_values('mean',ascending=False)
        stat = stat[stat['mean']!=0]
        stattail = stat.tail(10)[::-1]
        stathead = stat.head(10)

        px_bar = px.bar(stattail[["Title", "mean"]], x='Title', y='mean', title='Least Completed Games', labels = {'mean':'Average Completion Percentage'})
        st.plotly_chart(px_bar, use_container_width=True)

        px_bar = px.bar(stathead[["Title", "mean"]], x='Title', y='mean', title='Most Completed Games', labels = {'mean':'Average Completion Percentage'})
        st.plotly_chart(px_bar, use_container_width=True)

        st.write('''
        Based on the initial analysis of this data, we find that:
        - A very small percentage of people on average try to complete all the achievements in a game
        - This could potentially mean that a lot of achievements are post-game, so it could be used as a metric to identify the popularity of a game. If a community really likes a game, they'll try playing it to beyond 'completion'
        - This is further supported by the strongly left skewed first graph.
        ''')

        # age_grp = joined_data.groupby('Required_Age', as_index=False).mean()
        # st.pyplot(sns.lmplot(x="Required_Age", y="percentage", data=age_grp))

        st.markdown('''
                    ---
                    ''')
        #################################################################################################################

        st.subheader('Exploring Genres and Prices')
        st.write('Steam not only provides a marketplace for games but also for other softwares and tools.\n We\'ll first see the average prices and count of products within each type.')

        app_id_genre_info = app_ids_info.merge(games_genres, on=['appid'], how='left')
        app_id_genre_info['Release_Date'] = pd.to_datetime(app_id_genre_info['Release_Date'])
        ## Remove items with default timestamp unix timestamp (1970)
        app_id_genre_info = app_id_genre_info[app_id_genre_info['Release_Date'] != '1970-01-01']
        app_id_genre_info['Release_Year'] = app_id_genre_info['Release_Date'].dt.year


        type_price_info = app_id_genre_info.groupby('Type').agg(
        avg_price=('Price', 'mean'),
        item_count=('Price', 'count')
        ).reset_index()
        fig = px.scatter(type_price_info, x="Type", y="avg_price", size="item_count", hover_name="Type")
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig)

        st.write('Now we\'ll go deeper within each product type and the average prices of different genres within each type.')

        category = st.radio("Chose a product type", options=('game', 'dlc', 'video', 'mod'), key="category")
        category_df = app_id_genre_info[app_id_genre_info['Type'] == category][['Genre', 'Price']].groupby('Genre').mean().sort_values('Price').reset_index()
        px_bar = px.bar(category_df, x='Genre', y='Price', text='Price', title='Average Prices in $ across Genres')
        px_bar.update_traces(texttemplate='$%{text:.1f}', textposition='inside')
        px_bar.update_layout(uniformtext_minsize=5, uniformtext_mode='hide')
        st.plotly_chart(px_bar, use_container_width=True)

        st.write('Let us now see the average prices of single-payer and multiplayer games and DLCs.')

        relevant_genres = ['Casual', 'Indie', 'Free to Play', 'RPG', 'Simulation', 'Sports', 'Strategy', 'Adventure', 'Action', 'Racing', 'Massively Multiplayer']
        multiplayer_game = app_id_genre_info[(app_id_genre_info['Release_Year'] >=2010) & (app_id_genre_info['Type'] == 'game') & (app_id_genre_info['Genre'].isin(relevant_genres))][['Price','Is_Multiplayer']].groupby('Is_Multiplayer').mean()
        cols = st.columns(2)
        with cols[0]:
            st.metric(label="Multiplayer Game", value="$ {}".format(round(multiplayer_game['Price'][0], 2)))
        with cols[1]:
            st.metric(label="Singleplayer Game", value="$ {}".format(round(multiplayer_game['Price'][1], 2)))

        multiplayer_dlc = app_id_genre_info[(app_id_genre_info['Release_Year'] >=2010) & (app_id_genre_info['Type'] == 'dlc') & (app_id_genre_info['Genre'].isin(relevant_genres))][['Price','Is_Multiplayer']].groupby('Is_Multiplayer').mean()
        cols = st.columns(2)
        with cols[0]:
            st.metric(label="Multiplayer DLC", value="$ {}".format(round(multiplayer_dlc['Price'][0], 2)))
        with cols[1]:
            st.metric(label="Singleplayer DLC", value="$ {}".format(round(multiplayer_dlc['Price'][1], 2)))

        st.write('It can be seen that games and DLCs with a multiplayer component have higher mean prices than games without.')

        st.markdown('''
                    ---
                    ''')

        #################################################################################################################

        st.subheader("Exploring Game Publishers")

        topPublishers = game_publishers.groupby("publisher")["publisher"].count().reset_index(name="count").sort_values("count", ascending=False).head(20)
        bottomPublishers = game_publishers.groupby("publisher")["publisher"].count().reset_index(name="count").sort_values("count", ascending=True).head(20)
        topPublishers.plot.bar(x='publisher', y='count', xlabel='Popular Publishers', ylabel='Games Published', title='Apps Published by Top Publishers')
        bottomPublishers.plot.bar(x='publisher', y='count', xlabel='Popular Publishers', ylabel='Games Published', title='Apps Published by Bottom Publishers')

        games_combined = user_games.merge(game_publishers, how="left",left_on="appid", right_on="appId")
        games_combined["download_count"] = games_combined["appid"]
        top_downloads_publishers = games_combined.groupby("publisher").agg({"playtime_forever": "mean","download_count":"count"}).reset_index().sort_values(by="download_count", ascending=False).head(20)
        bottom_downloads_publishers = games_combined.groupby("publisher").agg({"playtime_forever": "mean","download_count":"count"}).reset_index().sort_values(by="download_count", ascending=True).head(20)

        top_downloads_publishers.plot.bar(x='publisher', y='download_count', xlabel='Publisher', ylabel='Total Downloads', title='Download Counts by Top Publishers')
        bottom_downloads_publishers.plot.bar(x='publisher', y='download_count', xlabel='Publisher', ylabel='Total Downloads', title='Download Counts by Bottom Publishers')


        games_combined = user_games.merge(game_publishers, how="left",left_on="appid", right_on="appId")
        games_combined["download_count"] = games_combined["appid"]
        top_downloads_publishers = games_combined.groupby("publisher").agg({"playtime_forever": "mean","download_count":"count"}).reset_index().sort_values(by="download_count", ascending=False).head(20)
        bottom_downloads_publishers = games_combined.groupby("publisher").agg({"playtime_forever": "mean","download_count":"count"}).reset_index().sort_values(by="download_count", ascending=True).head(20)

        top_downloads_publishers.plot.bar(x='publisher', y='download_count', xlabel='Publisher', ylabel='Total Downloads', title='Download Counts by Top Publishers')
        bottom_downloads_publishers.plot.bar(x='publisher', y='download_count', xlabel='Publisher', ylabel='Total Downloads', title='Download Counts by Bottom Publishers')

        top_downloads_publishers.plot.bar(x='publisher', y='playtime_forever', xlabel='Publisher', ylabel='Average Playtimes', title='Average Playtimes(mins) by Top Publishers')
        bottom_downloads_publishers.plot.bar(x='publisher', y='playtime_forever', xlabel='Publisher', ylabel='Average Playtimes', title='Average Playtimes(mins) by Bottom Publishers')


        st.write('Next we see the correlation between the number of titles published by different game publishers, the average playtime across these titles and the average number of times those titles were downloaded. Only the most popular 30 publishers in terms of the total playtime across their titles have been included for this analysis.')
        # games_combined_corr_df = games_combined.groupby("publisher").agg({"playtime_forever": "sum","playtime_forever": "mean","download_count":"sum", "appid":"count"}).sort_values(by="download_count", ascending=True).head(30)
        # games_combined_corr_df = games_combined.groupby("publisher").agg(playtime_forever=("playtime_forever", "sum"), playtime_forever_mean = ("playtime_forever", "mean"), download_count = ("download_count", "sum"), download_count_mean = ("download_count", "mean"), appid = ("appid", "count")).sort_values(by="download_count", ascending=True).head(30)
        games_combined_corr_df = games_combined.groupby("publisher").agg(playtime_forever_mean=("playtime_forever", "mean"), playtime_forever_sum=("playtime_forever", "sum"), download_count_mean = ("download_count", "mean"), appid_count = ("appid", "count")).sort_values(by="playtime_forever_sum", ascending=False).head(30).drop(columns=['playtime_forever_sum'])
        corr = games_combined_corr_df.corr()
        st.plotly_chart(px.imshow(corr,
                        x=['Average Playtime', 'Average Downloads', 'Total Published'],
                        y=['Average Playtime', 'Average Downloads', 'Total Published'],
                        labels={'color': 'Pearson\'s Coefficient'}
                    ))

        st.write('''
        - There is a positive correlation between the average downloads and average playtime across titles of a publisher which is expected.
        - There is a negative correlation between the average playtime across titles and the number of titles published which means that all the titles for most of the publishers are not equally popular. Only a few titles get the most playtime bringing down the average across the published titles.
        - There is a stronger negative correlation between the average downloads for the titles and the number of titles published which further proves that not all the titles of a particular publisher become popular. Only a few titles are downloaded the most bringing down the average download count across titles.
        ''')

        st.write('We will now see the total playtime of all the titles made by different publishers and how much they contribute to the total playtime on Steam. This will give an idea of the best publishers.')
        fig = px.treemap(games_combined.dropna(), path=[px.Constant("all"), 'publisher'], values='playtime_forever')
        fig.update_layout(margin = dict(t=10, l=25, r=25, b=10))
        st.plotly_chart(fig)

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
                    

        st.header("Data Processing and Cleaning")
        st.markdown('''
        - As described above, we first converted data from the SQL to CSV format.
        - Removed the index column as it is not used in any of our analysis.
        - Joined app_ID_Info and Acheievement_Percentages on app_id so that the entire relation is available easily for analysis.
        - Joined the app_id and name to see if there are any duplicate achievements and found that there were no repeated acheivements, which is great!
        - Dropped the columns `relationship` and `dateretrieved` from `Friends` data since the first one has only a constant value for all cases and the second one is not relevant to our analysis.
        - Dropped the rows with `friend_since` column less than 2009 since the field `friend_since` was added in 2009 and all the other entries before that had the epoch date set as a filler date.

            ''')
            
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

            