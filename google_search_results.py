import requests    #to send HTTP requests to internet
from bs4 import BeautifulSoup   #to parse the HTML content obtained from requests
import pandas as pd

#Give all the Search terms needes inside "Search_terms" list
#do not exceed 31 characters for each search term    
def extract_results(search_terms):    
    headers = {
     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    final_df = pd.DataFrame(columns=['Search Term','Category','Title','Linked Url'])
    for term in search_terms:
        r = requests.get(f"https://www.google.com/search?q={term}", headers = headers) #Google Search Request
        soup = BeautifulSoup(r.content, 'lxml') # Creating a BeautifulSoup Object
        
        #Extracting necessary Blocks of HTML Script by Categories from the BeautifulSoup Object
        news_stories = soup.find_all('a', class_='WlydOe')
        questions = soup.find_all('div', attrs={'jsname':'Cpkphb'})
        videos = soup.find_all('div', attrs={'jsname':'TFTr6'})
        urls =soup.find_all('div', class_='g Ww4FFb vt6azd tF2Cxc')
        ads = soup.find_all('div', class_='uEierd')
        places = soup.find_all('div', class_='VkpGBb')
    
        # diving into each extracted block of html script to get required information
        news_stories_list = []
        try:
            for story in news_stories:
                link = story['href']
                #for item in story.find('div', class_='mCBkyc tNxQIb ynAwRc nDgy9d'):
                 #   text = item.text
                text = story.find('div', class_='mCBkyc tNxQIb ynAwRc nDgy9d').text
                dict_story = {
                    "Search Term" : term,
                    "Category" : "News Stories",
                    "Title" : text,
                    "Linked Url": link
                    }
                news_stories_list.append(dict_story)     
        except:
            pass
            
        questions_list = []
        try:
            for question in questions:
                text = question.find('div', attrs = {'jsname':'jIA8B'}).text
                dict_questions = {
                    "Search Term" : term,
                    "Category" : "Questions",
                    "Title" : text,
                    "Linked Url" : None
                    } 
                questions_list.append(dict_questions)
        except:
            pass
        
        videos_list = []
        try:
            for video in videos:
                text = video.find('div', class_='fc9yUc tNxQIb ynAwRc OSrXXb').text
                link = video.find('a', class_='X5OiLe', href=True,ping = True)['href']
                dict_videos = {
                    "Search Term" : term,
                    "Category" : "Videos",
                    "Title" : text,
                    "Linked Url" : link
                    }
                videos_list.append(dict_videos)
        except:
            pass
            
        
        urls_list = []
        try:
            top_url = soup.find('div', class_='xpdopen')
            link = top_url.find('a', href=True)['href']
            text = top_url.find('h3', class_='LC20lb MBeuO DKV0Md').text
            dict_urls = {
                "Search Term" : term,
                "Category" : "Websites",
                "Title" : text,
                "Linked Url" : link
                }
            urls_list.append(dict_urls)
        except:
            pass   
        for url in urls:
            link = url.find('a', href=True)['href']
            text = url.find('h3', class_='LC20lb MBeuO DKV0Md').text
            dict_urls = {
                "Search Term" : term,
                "Category" : "Websites",
                "Title" : text,
                "Linked Url" : link
                }
            urls_list.append(dict_urls)
        
        ads_list = []
        try:
            for ad in ads:
                link = ad.find('a', class_='sVXRqc', href=True)['href']
                text = ad.find('div', class_ = 'CCgQ5 vCa9Yd QfkTvb MUxGbd v0nnCb').text
                dict_ads = {
                    "Search Term" : term,
                    "Category" : "Advertisements",
                    "Title" : text, 
                    "Linked Url" : link
                    }
                ads_list.append(dict_ads)
        except:
            pass
        
        places_list = []
        try:
            for place in places:
                text = place.find('div', class_ = 'dbg0pd').text
                link = place.find('a', class_='yYlJEf Q7PwXb L48Cpd', href=True)['href']
                dict_places = {
                    "Search Term" : term,
                    "Category" : "Places",
                    "Title" : text,
                    "Linked Url" : link
                    }
                places_list.append(dict_places)
        except:
            pass
        #Concat all the lists into a single consolidated list
        consolidated_results = urls_list + news_stories_list + videos_list + places_list + ads_list + questions_list  
        df_consolidated = pd.DataFrame(consolidated_results)     #passing consolidated list to a DataFrame
        # Create a Pandas Excel writer using XlsxWriter as the engine.        
        # Write each dataframe to a different worksheet.
        
        final_df = pd.concat([final_df,df_consolidated], axis = 0)
    return final_df