# -*- coding: utf-8 -*-
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import AgglomerativeClustering


baselink = 'https://www.flipkart.com'

def links_extraction(url_list,product,x):
    link = f'https://www.flipkart.com/search?q={product}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={x}'
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    
    links = soup.find_all('a', class_='_2rpwqI')
    if len(links)==0:
        links = soup.find_all('a', class_='_1fQZEK')

    for link in links:
        full_url = baselink + link['href']
        url_list.append(full_url)
        
#ls = []
#for x in range(1,4):
#    links_extraction(ls,'face wash',x)
    
def product_details(product_information_list,url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    
    try:
        name = soup.find('span', class_='B_NuCI').text
    except:
        name = None
    try:
        ratings_reviews = soup.find('div', class_='gUuXy- _16VRIQ')
    except:
        ratings_reviews = None
    try:
        rating = ratings_reviews.find('div', class_='_3LWZlK').text
    except:
        rating = None
        
    try:
        numbers = ratings_reviews.find('span', class_='_2_R_DZ').text
    except:
        numbers = None
    
    try:
        price_info = soup.find('div', class_='CEmiEU')
    except:
        price_info = None
    
    try:
        striked_price = price_info.find('div', class_='_3I9_wc _2p6lqe').text
    except:
        striked_price = None
        
    try:
        listed_price = price_info.find('div', class_='_30jeq3 _16Jk6d').text
    except:
        listed_price = None
        
    product_dict = {
        "Name" : name,
        "Rating Stars" : rating,
        "Rating and Review Numbers" : numbers,
        "Striked Price" : striked_price,
        "Listed Price" : listed_price
        }
    
    product_information_list.append(product_dict)


    
def data_processing(data_list):
    df = pd.DataFrame(data_list)
    df.dropna(axis='index', how='all', inplace=True) 
    df.dropna(axis='index', how='all', subset = ['Rating Stars','Rating and Review Numbers'],inplace = True) 
    df2 = df.drop_duplicates()
    df2['Striked Price']= df2['Striked Price'].fillna(0)

    df2['Striked Price'] = df2['Striked Price'].str.replace(r'(\D)','',regex=True)
    df2['Listed Price'] = df2['Listed Price'].str.replace(r'(\D)','',regex=True)

    df2[['Ratings Count','Reviews Count']] = df2['Rating and Review Numbers'].str.extract(r'(\S+)\sRatings\s&\s(\S+)\sReviews')

    df2['Ratings Count'] = df2['Ratings Count'].str.replace(r'(\D)','',regex=True)
    df2['Reviews Count'] = df2['Reviews Count'].str.replace(r'(\D)','',regex=True)

    df2['MRP'] = np.where(df2['Striked Price'].isna(),df2['Listed Price'],df2['Striked Price'])
    df2['Discounted Price'] = df2['Listed Price']

    df2[["Ratings Count", "Reviews Count","MRP","Discounted Price"]] = df2[["Ratings Count", "Reviews Count","MRP","Discounted Price"]].apply(pd.to_numeric)
    df2['Discount Percentage'] = round(((1-(df2['Discounted Price']/df2['MRP']))*100),0)

    df2.drop(columns=['Rating and Review Numbers', 'Striked Price','Listed Price'],inplace=True)
    
    return df2

def remove_name(data_frame):
    cluster_df = data_frame.drop(columns=['Name'])
    cluster_df.reset_index(inplace = True)
    cluster_df.drop(columns=['index'],inplace=True)
    return cluster_df
    
def normalization(data_frame):
    def norm_func(i):
        x = (i-i.min())	/ (i.max()-i.min())
        return (x)
    df_norm = norm_func(data_frame.iloc[:, 1:])
    
    return df_norm

def hierarchical_linkage(normalized_dataframe):   
    z = linkage(normalized_dataframe, method = "complete", metric = "euclidean")
    return z

def hierarchical_clustering(original_dataframe,normalized_dataframe,cluster_count):
    h_complete = AgglomerativeClustering(n_clusters = cluster_count, linkage = 'complete', affinity = "euclidean").fit(normalized_dataframe) 
    cluster_labels = pd.Series(h_complete.labels_)
    original_dataframe['cluster labels'] = cluster_labels
    
    return original_dataframe,cluster_labels


