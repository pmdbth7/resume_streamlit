# Data Science Projects run with Streamlit
#### App can be accessed here -> [Streamlit Web App](https://pmdbth7-resume-streamlit-app-hlx62r.streamlit.app/)
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

### 3. Scraping Google Search Results Page
* **Modules/Libraries used :** Requests, BeautifulSoup and Pandas
* **Objective :** to collect, categorize and store the search results of google
* **Process Involved :**
  * Use Requests Library to collect information on search page of google search engine
  * Traverse through the content and get required information with BeautifulSoup Objects
  * Categorize the content and name it accordingly, for e.g. websites, advertisements, news stories, videos etc...
  * store the data on the cloud/in a database for subsequest comparison.
* **Use Case :** To validate your SEO techniques
