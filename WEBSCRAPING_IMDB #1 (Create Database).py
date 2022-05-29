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
    passwd = "root"
    )

mycursor = db.cursor()

# ------------- CREATE A DATABASE  -------------
mycursor.execute("CREATE DATABASE webscraping_db")



# ---------- CHECK DATABASE IS CREATED ---------
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)



