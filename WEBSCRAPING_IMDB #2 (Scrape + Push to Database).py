import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import statistics


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
    database = "webscraping_db"
    )

mycursor = db.cursor()


i=0
count=0
rank = []
title = []
year = []
rating = []
runtime = []
votes = []

metascore = []
directors = []
stars = []

substring_1 = 'Director'
substring_2 = 'Directors'

pages = np.arange(1,250,50)

#-------------- Scrape Multiple Webpages ------------
for page in pages:
    #original_url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating'
    url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start='+str(page)+'&ref_=adv_nxt'
    response = requests.get(url)
    #print(response.content)
    soup = BeautifulSoup(response.content,'html.parser') 
    
    movie_data = soup.findAll('div', attrs={'class':'lister-item mode-advanced'})

    for store in movie_data:
        count+=1
        rank.append(count)
        
        title_temp = store.h3.a.text
        title.append(title_temp)

        year_temp = store.h3.find('span', class_= 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        year_temp = year_temp.replace("I ","")
        year.append(int(year_temp))

        runtime_temp = store.p.find('span', class_='runtime').text.replace(' min','')
        runtime.append(int(runtime_temp))

        rating_temp = store.find('div', class_='inline-block ratings-imdb-rating').strong.text
        rating.append(float(rating_temp))

        votes_temp = store.find_all('span', attrs = {'name': 'nv'}) if store.find_all('span', attrs={'name': 'nv'}) else 'NA'
        votes.append(votes_temp[0].text)
                                                                   
        directors_temp = str(store.find('p', class_= ''))  # Convert to soup --> string
        
        if substring_2 in directors_temp:  # Check if string contains "Directors"
            split_string = directors_temp. split("<span", 1) # Remove everything after <span
            soup_directors = BeautifulSoup(split_string[0],'html.parser')  # Convert string --> soup
            
            
            for d in soup_directors:
                directors_temp = d.text
                directors_temp = str(directors_temp)
                split_string = directors_temp.split("Directors:",1)
                joined_string = ''.join(split_string[1])
                joined_string = joined_string.replace("\n","")
            directors.append(joined_string)
            
        elif substring_1 in directors_temp: # If string contains "Director"
            directors_temp = str(store.find('p', class_=''))
            split_string = directors_temp. split("<span", 1) # Remove everything after <span
            soup_directors = BeautifulSoup(split_string[0],'html.parser')  # Convert string --> soup
            
            
            for d in soup_directors:
                directors_temp = d.text
                directors_temp = str(directors_temp)
                split_string = directors_temp.split("Director:",1)
                split_string[1] = split_string[1].replace("\n","")
                
            directors.append(split_string[1])
            
            
            
        
                                                                      
    movie_DF = pd.DataFrame({'Rank':rank ,'Movie':title, 'Release_Year':year, 'Runtime':runtime, 'Rating':rating, 'Votes':votes, 'Directors':directors})
        


sql_engine = create_engine("mysql+mysqldb://root:root@localhost/webscraping_db")

#------------- Push Data to Sql Database ----------

movie_DF.to_sql(con=sql_engine, name='imdb', if_exists='replace', index=False)





























#------------- USELESS CODE LEFT HERE FOR FUTURE REFERENCE ----------
#mycursor.execute("DROP DATABASE imdb")
#mycursor.execute("CREATE TABLE IMDB (Movie VARCHAR(50), Release_Year smallint UNSIGNED, Runtime int UNSIGNED, Rating int UNSIGNED, Votes int UNSIGNED, Movie_ID int PRIMARY KEY AUTO_INCREMENT)")


#mycursor.execute("DESCRIBE IMDB")
#for x in mycursor:
#    print(x)
#movie_DF.head(30)
#print(movie_DF)    
#np.count_nonzero(title)




    

