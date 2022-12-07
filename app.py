# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_option_menu import option_menu
import google_search_results as glg
import base64
import flipkart 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import snscrape.modules.twitter as snt
import re
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import silhouette_score

st.set_page_config(layout="wide")

@st.cache()
def load_pack_warn():
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    

load_pack_warn()

selected = option_menu(
    menu_title = None, 
    options = ['Info','Twitter NLP',
               'Flipkart product analysis',
               'Google results extraction'],
    icons = ['bookmarks','twitter','bag-check',
             'google'],              # icons are taken from  https://icons.getbootstrap.com/
    menu_icon = 'menu-up',
    default_index = 0,
    orientation='horizontal'
    )

load_pack_warn()

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download CSV File</a>'
    return href


if selected == 'Info':
    st.subheader('The contents of this streamlit web application are as follows')
    col1,col2,col3 = st.columns(3)
    col1.markdown('''
                ### 1. NLP with Twitter
                * **Modules/Libraries used :** Snscrape, Pandas, NLTK, Wordcloud, Matplotlib, RegularExpressions
                * **Objective :** To collect, process, analyze, and visualize any number of tweets for a given search word
                * **Process Involved :**
                    * collect the tweets from the given search query
                    * filter out the tweets with english language
                    * processing the text with methods such as RegularExpressions, Tokenization, Lemmitization, Stopwords Removal
                    * Visualize 3 wordclouds consisting of unfiltered, positive and negative words
                    * display top 5 tweets by like, replies, retweets within the colledtec tweets
                * **Use Case :** Social Media Sentiment analysis 
                ''')
    col2.markdown('''
                ### 2. Clustering with Flipkart Product data
                * **Modules/Libraries used :** Requests, Pandas, BeautifulSoup, Matplotlib, Scipy, Sklearn, Numpy
                * **Objective :** To Collect product data from flipkart ecommerce website and apply hierarchihcal clustering to segregrate the products
                * **Process Involved :** 
                    * Gather product data from flipkart through web scraping 
                    * collect attributes such as price, discount, count of ratings and reviews
                    * process the data to discard/impute any unwanted or null values
                    * normalize the data for hierarchical clustering
                    * change the no:of clusters until a good Silhoutte Score is obtained.
                * **Use Case :** To dived the products into groups such as high selling/low selling, most liked/least liked and divide the teams attention and resourced accordingly
                * **P.S. :** The efficiency and uses of the created clusters is subjective and depends on users needs.
                ''')
    col3.markdown('''
                ### 3. Scraping Google Search Results Page
                * **Modules/Libraries used :** Requests, BeautifulSoup and Pandas
                * **Objective :** to collect, categorize and store the search results of google
                * **Process Involved :**
                    * Use Requests Library to collect information on search page of google search engine
                    * Traverse through the content and get required information with BeautifulSoup Objects
                    * Categorize the content and name it accordingly, for e.g. websites, advertisements, news stories, videos etc...
                    * store the data on the cloud/in a database for subsequest comparison.
                * **Use Case :** To validate your SEO techniques
                ''')
    pass
############################################################################################################################
if selected == 'Twitter NLP':
        st.markdown('''
                    ## Please Provide data into the sidebar and hit search
                    ### Refer to Currents trends on twitter
                    ''')
        trends_list = []
        st.sidebar.title('Sidebar')
        
        def wordcloud(ip_string):
            wordcloud = WordCloud(background_color='White',
                              width=900,
                              height=1400
                             ).generate(ip_string)
            return wordcloud
        
        @st.cache()
        def get_trends():
            trends = snt.TwitterTrendsScraper().get_items()
            for trend in trends:
                trends_list.append([trend.name,trend.domainContext,trend.metaDescription])
            trend_df = pd.DataFrame(trends_list,columns=['Trend','Context','No:of tweets'])
            return trend_df
        
        trends = get_trends()
        st.write(trends)
        
        query = st.sidebar.text_input('enter your search here', placeholder='e.g. #formula1 or FifaWorldCup')
        tweets_count = st.sidebar.text_input('enter the count of tweets', placeholder='e.g. 250 or 500 or 1000')
        user_stopwords = st.sidebar.text_area('enter unwanted words to filter out seperated by a comma',placeholder = 'e.g. football, soccer, qatar2022 are most likely expected when you search for fifa')
        
        button = st.sidebar.button('search')
        
        @st.cache(suppress_st_warning=True)
        def get_tweets(query,tweets_count):
            generator = snt.TwitterSearchScraper(query).get_items()
            tweets_list = []
            limit = int(tweets_count)
            progress = st.progress(0)
            
            for tweet in generator:
                if len(tweets_list) == limit:
                    break
                else:
                    tweets_list.append([tweet.date, tweet.username, tweet.content, tweet.lang,tweet.likeCount,
                            tweet.replyCount,tweet.retweetCount])
                perct = int((len(tweets_list)/limit)*100)
                progress.progress(perct)
            
            df = pd.DataFrame(tweets_list, columns=['Date', 'User', 'Tweet','Language','Likes','Replies','Retweets'])
            return df

        if button and query and tweets_count :
            st.markdown(f'Collecting **{tweets_count}** tweets for **{query}**')
            df = get_tweets(query, tweets_count)
            
            st.markdown(f'download the tweets into a csv file here ->{filedownload(df)}', unsafe_allow_html=True)
            eng_df = df[df['Language'] == 'en']
            
            tw = eng_df['Tweet']

            tw = list(tw)

            ip = " ".join(tw)

            ip = re.sub(r'((?:http)|(?:@)|(?:#))\S*', '', ip)
            ip = re.sub("[^A-Za-z" "]+", " ", ip).lower()

            ip_words = ip.split(" ")
            ip_words = ip_words[1:]
            
            with open("stop.txt", "r") as pos:
                stop_words = pos.read().split("\n")
            
            #stop_words = list(stopwords.words('english'))
            search_words = [word.strip().lower() for word in query.split(',')]
            stop_words.extend(search_words)
            
            
            custom_stopwords = [word.strip().lower() for word in user_stopwords.split(',')]
            stop_words.extend(custom_stopwords)
            
            lemmatizer = WordNetLemmatizer()
            ip_words = [lemmatizer.lemmatize(word) for word in ip_words]
            
            ip_words = [w.strip()for w in ip_words if not w in stop_words]

            ip_string = " ".join(ip_words)
            
            with open("positive-words.txt", "r") as pos:
                poswords = pos.read().split("\n")
            ip_pos = " ".join ([w.strip() for w in ip_words if w in poswords])
            
            with open("negative-words.txt", "r") as neg:
                negwords = neg.read().split("\n")
            ip_neg = " ".join ([w.strip() for w in ip_words if w in negwords])
            
        if query and button and tweets_count:
            
            col1,col2,col3 = st.columns(3)
            
            col2.subheader('General wordcloud')
            col1.subheader('positive wordcloud')
            col3.subheader('negative wordcloud')
            
            wordcloud_ip = wordcloud(ip_string)
            plt.imshow(wordcloud_ip)
            plt.axis('off')
            col2.pyplot()
            
            
            wordcloud_pos_in_pos = wordcloud(ip_pos)
            plt.imshow(wordcloud_pos_in_pos)
            plt.axis('off')
            col1.pyplot()
            
            wordcloud_neg_in_neg = wordcloud(ip_neg)
            plt.imshow(wordcloud_neg_in_neg)
            plt.axis('off')
            col3.pyplot()
            
            st.sidebar.subheader('Update filtered words in the text area above to remove any unwanted words form the WordClouds')
            
            st.markdown('### Top Tweets with most Likes, Replies and Retweets in the collected data')
            col1,col2,col3 = st.columns(3)
            col1.subheader('Top likes')
            col1.write(eng_df.sort_values('Likes',ascending = False)[['User','Tweet','Likes']].head(5))
            col2.subheader('Top Replies')
            col2.write(eng_df.sort_values('Replies',ascending = False)[['User','Tweet','Replies']].head(5))
            col3.subheader('Top Retweets')
            col3.write(eng_df.sort_values('Retweets',ascending = False)[['User','Tweet','Retweets']].head(5))
        st.subheader('Please enter or change data in the sidebar for more analysis')
##############################################################################################################################################
if selected == 'Flipkart product analysis':
        st.header('Enter data into the Sidebar and hit search')
        
        #st.sidebar.title('options')
        name = st.sidebar.text_input('enter your product name',placeholder = 'e.g. shampoo, soaps, laptops')
        pages = st.sidebar.slider('choose no:of pages that you need data from',1,40,1)
        sidebar_clusters = st.sidebar.slider('Choose no:of clusters',1,10,1)
        st.sidebar.write('if the the above slider is at 1 then no:of clusters is choosen based on count of colors in dendrogram - 1')
        
        search = st.sidebar.button('search')
        
        product_info = []
        @st.cache(suppress_st_warning=True)
        def data_extraction(query,pages_count):
            product_info_list = []
            urls = []
            for x in range(1,pages_count+1):
                flipkart.links_extraction(urls,query,x)
            
            
            st.subheader('Extracting information')
            prg2 = st.progress(0)
            for url in urls:
                flipkart.product_details(product_info_list, url)
                perct = (len(product_info_list)/len(urls))*100
                prg2.progress(int(perct))
            
            return product_info_list
            
        if search and name:
            product_info = data_extraction(name, pages)
        
            st.subheader('processing data and creating dendrogram')
            
        col1,col2 = st.columns(2)
        if len(product_info)>1:
            
            df = flipkart.data_processing(product_info)
            col1.write(df)
            col1.markdown(f'Download the above collected information here -> {filedownload(df)}', unsafe_allow_html=True)
            
            
            df_name_rem = flipkart.remove_name(df)
            
            #st.subheader('Clustering of products')
            
            df_normalized = flipkart.normalization(df_name_rem)
            
            linkage = flipkart.hierarchical_linkage(df_normalized)
            
            
            dendrogram_h = dendrogram(linkage, 
                leaf_rotation = 0,  # rotates the x axis labels
                leaf_font_size = 0 # font size for the x axis labels
            )
            col2.pyplot()
            if sidebar_clusters == 1:
                clusters_count = len(set(dendrogram_h['color_list'])) - 1
            else:
                clusters_count = sidebar_clusters

            hierarchical_dataframe,cluster_labels = flipkart.hierarchical_clustering(df_name_rem,df_normalized , clusters_count)
            st.subheader('Number of products for each cluster')
            st.write(hierarchical_dataframe['cluster labels'].value_counts())
            try:
                st.sidebar.markdown(f'''
                                   ## Silhoutte score : {silhouette_score(df_name_rem,cluster_labels)}
                                   * if the Silhoutte Score is low or negative change the no:of clusters and hit search again
                                   * refer to this article for optimal [Silhoutte Score](https://towardsdatascience.com/silhouette-coefficient-validating-clustering-techniques-e976bb81d10c#:~:text=Silhouette%20Coefficient%20or%20silhouette%20score%20is%20a%20metric%20used%20to,each%20other%20and%20clearly%20distinguished.)
                                    ''')
                #st.sidebar.markdown(silhouette_score(df_name_rem,cluster_labels))
            except:
                st.sidebar.markdown('''
                                    * the clusters are less than two so no silhoutte score
                                    * change the no:of clusters and try again
                                    * refer to this article for optimal [Silhoutte Score](https://towardsdatascience.com/silhouette-coefficient-validating-clustering-techniques-e976bb81d10c#:~:text=Silhouette%20Coefficient%20or%20silhouette%20score%20is%20a%20metric%20used%20to,each%20other%20and%20clearly%20distinguished.)
                                    ''')
                pass
            
            st.subheader('Refer to the pandas describe method for each created cluster below')
            for x in range(clusters_count):
                st.text(f"cluster number {x+1}")
                st.write(hierarchical_dataframe[hierarchical_dataframe['cluster labels'] == float(x)].describe())
            
         
       
#############################################################################################################################################
if selected == 'Google results extraction':
        st.title('Enter the search words into the side bar seperated by comma')
        
        st.sidebar.header('google')
        csv = st.sidebar.text_input('enter you search words seperated by comma',"")
        search = st.sidebar.button('Search')
        search_list = []
        if search:
            search_list = csv.split(',')
            
        if len(search_list)>0:
            results  = glg.extract_results(search_list)

            result_types = ['Websites','News Stories','Videos','Questions','Advertisements','Places']
            
            rows = []
            for term in search_list:
                value = []
                value.append(term)
                for type in result_types:
                    count = results[(results['Search Term'] == term) & 
                                    (results['Category']==type)]['Category'].count()
                    value.append(count)
                rows.append(value)
            
            results_summary_columns = ['term','Websites','News Stories','Videos',
                                       'Questions','Advertisements','Places']
            results_summary = pd.DataFrame(rows,columns = results_summary_columns)
            
            if len(results)>1:
                st.subheader('Summary of the results')
                st.write(results_summary)
                st.subheader('results preview')
                st.write(results)
                st.markdown(f'download you results into csv file here -> {filedownload(results)}', unsafe_allow_html=True)
            else:
                st.markdown('''
                            ## Oops..! No data extracted
                            ### Google domain might've hit Captcha page
                            ### please try again after sometime..!
                            ''')
        
        
        
             
        

