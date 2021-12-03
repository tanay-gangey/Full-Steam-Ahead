from mysql.connector import MySQLConnection, Error    
from python_mysql_dbconfig import read_db_config
import pandas as pd


# Open the file
f = open('Friends.csv', 'w')
# Create a connection and get a cursor
dbconfig = read_db_config()
print(dbconfig)
connection = MySQLConnection(**dbconfig)

#connection = sqlite3.connect('steam')
cursor = connection.cursor()
#print(cursor)
# Execute the query
cursor.execute('select * from Friends')
# Get data in batches
while True:
    # Read the data
    df = pd.DataFrame(cursor.fetchmany(1000))
    #print(df)
    # We are done if there are no data
    if len(df) == 0:
        break
    # Let's write to the file
    else:
        df.to_csv(f, header=False)

# Clean up
f.close()
cursor.close()
connection.close()
