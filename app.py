import json
import requests
from attr import has
import streamlit as st
from streamlit_lottie import st_lottie
from helper import preprocessing_data, graph_sentiment, analyse_mention, analyse_hastag, download_data, commonword, commonwordlist, intersection

st.set_page_config(
     page_title="Data Analysis Web App",
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded",
    
)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://wallpapercave.com/wp/wp3328592.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_bo8vqwyw.json")


st.markdown("<h1 style='text-align: center; color:  white;'>Twitter Personality Analysis</h1>", unsafe_allow_html=True)
 



function_option = st.sidebar.selectbox("Select The Funtionality: ", ["Search By #Tag and Words", "Search By Username"])

if function_option == "Search By #Tag and Words":
    st.markdown("<p style='color: white;'>Enter the Hashtag or any word:</p>", unsafe_allow_html=True)
    word_query = st.text_input("", key="hashtag_input")

if function_option == "Search By Username":
    st.markdown("<p style='color: white;'>Enter the Username (Don't include @):</p>", unsafe_allow_html=True)
    word_query = st.text_input("", key="username_input")



st.markdown(
    "<label style='color: white;'>How many tweets You want to collect from {}</label>".format(word_query), 
    unsafe_allow_html=True)
number_of_tweets = st.slider("", min_value=100, max_value=10000, value=1000)
st.markdown("<p style='color: white;'>1 Tweet takes approximately 0.05 seconds to collect, so you may have to wait {} minutes for {} Tweets. Please be patient.</p>".format(round((number_of_tweets*0.05/60),2), number_of_tweets), 
            unsafe_allow_html=True)


if st.button("Analyze Sentiment"):

    st_lottie(
    lottie_hello,
    speed = 1,
    reverse = False,
    loop = True,
    quality = "high",
    #renderer = "Any",
    height= 300,
    width= None,
    key= None,
)

    data = preprocessing_data(word_query, number_of_tweets, function_option)
    analyse = graph_sentiment(data)
    mention = analyse_mention(data)
    hastag = analyse_hastag(data)

    st.write(" ")
    st.write(" ")
    st.header("Here are the tweets we analyzed")
    st.write(data)
    download_data(data, label="twitter_sentiment_filtered")
    st.write(" ")
    
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("### We analyzed it! See the results below!")
    
    st.subheader("Twitter Sentiment Analysis")
    st.bar_chart(analyse)


    col1, col2 = st.columns(2)

    with col1:
        st.text("Top 10 @Mentions in {} tweets".format(number_of_tweets))
        st.bar_chart(mention)
    with col2:
        st.text("Top 10 Hastags used in {} tweets".format(number_of_tweets))
        st.bar_chart(hastag)
    
    col3, col4 = st.columns(2)
    with col3:
        st.text("Top 10 Used Links for {} tweets".format(number_of_tweets))
        st.bar_chart(data["links"].value_counts().head(10).reset_index())
    
    with col4:
        st.text("All the Tweets that containes top 10 links used")
        filtered_data = data[data["links"].isin(data["links"].value_counts().head(10).reset_index()["index"].values)]
        st.write(filtered_data)
    
   