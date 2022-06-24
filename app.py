import streamlit as st
import pandas as pd
import DataPreprocessor,MedalTally,OverallAnalysis,NationStatistics,AthleteStatistics
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import time

dataFrame = pd.read_csv('datasets/athlete_events.csv')
region_dataFrame = pd.read_csv('datasets/noc_regions.csv')

dataFrame = DataPreprocessor.preprocess(dataFrame,region_dataFrame)

st.sidebar.header("Interactive Summer Olympic Analysis")
st.sidebar.image('https://www.pngfind.com/pngs/m/108-1088495_all-professional-and-major-sports-supported-olympics-logo.png')
user_option = st.sidebar.radio(
    'Select an Option',
    ("Overview",'Overall Analysis','Nation-wise Analysis','Athlete-wise Analysis','Medal Tally')
)

if user_option=="Overview":
    st.header("What is this about?")
    st.write("This is an interactive web application that analyses the Summer Olympic Games from 1896 to 2016. Get a quick rundown of the summer Olympic statistics here. Play around with the visuals here to get results for the analysis of your choice.")
  
    st.subheader("Overall Analysis")
    st.write("Learn about the sporting events, the various sports that have been included over the years, and the level of participation by the countries over time. Over the course of the Olympics, discover the most accomplished athletes.")
   
    st.subheader("Nation-wise Analysis")
    st.write("Learn how your favourites have performed over time. Take a look at how a certain nation's total number of medals has changed throughout time. Which sporting event does a specific nation do well and Learn about the top ten athletes in a given nation.")
  
    st.subheader("Athlete-wise Analysis")
    st.write("Learn about the differences in participation between men and women. Do you know which age group, overall or in a given sport, wins the most medals? What impact do an athlete's height and weight have on whether they'll win a medal?")

    st.subheader("Medal Tally")
    st.write("Change the two analysis parameters for yourself to learn more about which country has the most medals. Find out a country's overall or specific medal total.")

if user_option == 'Overall Analysis':
    editions = dataFrame['Year'].unique().shape[0] - 1
    cities = dataFrame['City'].unique().shape[0]
    sports = dataFrame['Sport'].unique().shape[0]
    events = dataFrame['Event'].unique().shape[0]
    athletes = dataFrame['Name'].unique().shape[0]
    nations = dataFrame['region'].unique().shape[0]

    st.header("Important Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader("Editions")
        st.header(editions)
    with col2:
        st.subheader("Hosts")
        st.header(cities)
    with col3:
        st.subheader("Sports")
        st.header(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Events")
        st.header(events)
    with col2:
        st.subheader("Nations")
        st.header(nations)
    with col3:
        st.subheader("Athletes")
        st.header(athletes)

    nations_over_time = OverallAnalysis.data_over_time(dataFrame,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.header("Participating Nations over the years")
    st.plotly_chart(fig)

    st.header("Most successful Athletes")
    sport_list = dataFrame['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Choose a Sport',sport_list)
    x = OverallAnalysis.most_successful(dataFrame,selected_sport)
    x.reset_index(inplace=True,drop=True)
    x.index = x.index +1
    st.table(x)

    events_over_time = OverallAnalysis.data_over_time(dataFrame, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.header("Sporting Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = OverallAnalysis.data_over_time(dataFrame, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.header("Athletes over the years")
    st.plotly_chart(fig)

    st.header("Number of Events over time")
    fig,ax = plt.subplots(figsize=(20,20))
    x = dataFrame.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)


if user_option == 'Nation-wise Analysis':

    st.sidebar.header('Nation-wise Analysis')

    country_list = dataFrame['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    if st.sidebar.button("Submit"):
            with st.spinner('Wait for it...'):
                time.sleep(1)
                country_dataFrame = NationStatistics.yearwise_medal_tally(dataFrame,selected_country)
                fig = px.line(country_dataFrame, x="Year", y="Medal")
                st.header(selected_country + " Medal Tally over the years")
                st.plotly_chart(fig)

                st.header("Top 10 athletes of " + selected_country)
                top10_dataFrame = NationStatistics.most_successful_countrywise(dataFrame,selected_country)
                top10_dataFrame.reset_index(inplace=True,drop=True)
                top10_dataFrame.index = top10_dataFrame.index +1
                st.table(top10_dataFrame)

                st.header(selected_country + " excels in the following sports")
                pt = NationStatistics.country_event_heatmap(dataFrame,selected_country)
                fig, ax = plt.subplots(figsize=(20, 20))
                try:
                    ax = sns.heatmap(pt,annot=True)
                    st.pyplot(fig)
                except ValueError as ve:
                    st.write("Not Much Contribution")



if user_option == 'Athlete-wise Analysis':
    
    
    athlete_dataFrame = dataFrame.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_dataFrame['Age'].dropna()
    x2 = athlete_dataFrame[athlete_dataFrame['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_dataFrame[athlete_dataFrame['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_dataFrame[athlete_dataFrame['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.header("Age Distribution")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_dataFrame = athlete_dataFrame[athlete_dataFrame['Sport'] == sport]
        x.append(temp_dataFrame[temp_dataFrame['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = dataFrame['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.header('Height Vs Weight Medal Achievement')
    selected_sport = st.selectbox('Choose a Sport', sport_list)
    temp_dataFrame = AthleteStatistics.weight_v_height(dataFrame,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_dataFrame['Weight'],temp_dataFrame['Height'],hue=temp_dataFrame['Medal'],style=temp_dataFrame['Sex'],s=60)
    st.pyplot(fig)

    st.header("Men Vs Women Participation Over the Years")
    final = AthleteStatistics.men_vs_women(dataFrame)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

if user_option == 'Medal Tally':
    st.sidebar.subheader("Medal Tally")
    years,country = MedalTally.country_year_list(dataFrame)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Nation", country)

    medal_tally = MedalTally.fetch_medal_tally(dataFrame,selected_year,selected_country)
    if st.sidebar.button("Submit"):
        with st.spinner('Wait for it...'):
            time.sleep(1)
            if selected_year == 'Overall' and selected_country == 'Overall':
               st.header("Overall Medal Tally")
            if selected_year != 'Overall' and selected_country == 'Overall':
                st.header("Medal Tally in " + str(selected_year) + " Olympics")
            if selected_year == 'Overall' and selected_country != 'Overall':
                st.header(selected_country + " overall performance")
            if selected_year != 'Overall' and selected_country != 'Overall':
                st.header(selected_country + " performance in " + str(selected_year) + " Olympics")
            medal_tally.reset_index(inplace=True,drop=True)
            medal_tally.index +=  1
            st.table(medal_tally)


