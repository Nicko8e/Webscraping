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


sql_engine = create_engine("mysql+mysqldb://root:root@localhost/webscraping_db")



#---------- Query from SQL database to Python ----------
query = "SELECT Runtime, Rating FROM imdb"
mycursor.execute(query)
result = mycursor.fetchall()

runtime = [i[0] for i in result]
rating = [i[1] for i in result]

runtime_mean = statistics.mean(runtime)
runtime_sd = statistics.stdev(runtime)
print(runtime_mean)
print(runtime_sd)


# ---------- Plot Data ---------------


plt.hist(runtime, bins=50, color='b')

plt.axvline(runtime_mean, color='k', linestyle='dashed')
plt.axvline(runtime_mean + runtime_sd, color='y', linestyle='dashed')
plt.axvline(runtime_mean - runtime_sd, color='y', linestyle='dashed')

plt.xlabel("Runtime")
plt.ylabel("Frequency")
plt.title("Runtime Histogram")
plt.show()




























#------------- USELESS CODE LEFT HERE FOR FUTURE REFERENCE ----------
#mycursor.execute("DROP DATABASE imdb")
#mycursor.execute("CREATE TABLE IMDB (Movie VARCHAR(50), Release_Year smallint UNSIGNED, Runtime int UNSIGNED, Rating int UNSIGNED, Votes int UNSIGNED, Movie_ID int PRIMARY KEY AUTO_INCREMENT)")


#mycursor.execute("DESCRIBE IMDB")
#for x in mycursor:
#    print(x)
#movie_DF.head(30)
#print(movie_DF)    
#np.count_nonzero(title)




    

