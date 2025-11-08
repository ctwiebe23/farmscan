import sqlite3

conn = sqlite3.connect('./app/db/soil_data.sqlite')
cursor = conn.cursor()
result = cursor.execute("select * from joined_layer")
print(result.fetchone())