import sqlite3

try:
    # Making a connection between sqlite3 database and Python Program
    conn = sqlite3.connect('linkedin_jobs.db')

    curs = conn.cursor()

    sql_command = """
    );"""

    curs.execute(sql_command)


    print("Connected to SQLite and query successfully executed")

except sqlite3.Error as error:
    print("Failed to connect with sqlite3 database", error)

finally:
    # Inside Finally Block, If connection is open, we need to close it
    if conn:
        conn.close()
        # using close() method, we will close the connection
        # After closing connection object, we will print "the sqlite connection is closed"
        print("the SQLite connection is closed")
