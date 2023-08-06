import sqlite3 as sq
 
# Import pandas module into
# this program as pd
import pandas as pd
   
# Create a connection object,
# Make a new db if not exist already 
# and connect it, if exist then connect.
def Astrolib(date):
  connection = sq.connect('Astrology.db')
  # Create a cursor object
  curs = connection.cursor()
  # Run create table sql query
  curs.execute("create table if not exists Planets" +
             " (Date text, Sun text,Moon text,Mercury text,Venus text,Mars text,Jupiter text,Saturn text,Uranus text,Neptune text,Pluto text,mean_Node text)")
  # Load CSV data into Pandas DataFrame
  student = pd.read_csv("./Planets.csv")
  # Write the data to a sqlite db table
  student.to_sql('Planets', connection, if_exists='replace', index=False)
  
  curs.execute("SELECT * FROM Planets WHERE Date=?", (date,))
  rows=curs.fetchall() 
  for row in rows:
    print("Sun: "+str(row[1]))
    print("Moon: "+str(row[2]))
    print("Mercury: "+str(row[3]))
    print("Venus "+str(row[4]))
    print("Mars "+str(row[5]))
    print("Jupiter "+str(row[6]))
    print("Saturn "+str(row[7]))
    print("Uranus "+str(row[8]))
    print("Neptune"+str(row[9]))
    print("Pluto "+str(row[10]))
    print("Mean Node "+str(row[11]))
    print("")
  # Close connection to SQLite database
  connection.close()
date=input("Enter Date(IN YYYYMMDD Format):")  #Testing:Enter Date 20000102
Astrolib=Astrolib(date)
