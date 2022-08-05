import sqlite3

try:
    # Making a connection between sqlite3 database and Python Program
    conn = sqlite3.connect('linkedin_jobs.db')

    curs = conn.cursor()

    sql_command = """CREATE TABLE linkedin_jobs (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME,
        job_title TEXT,
        company TEXT,
        location TEXT,
        link TEXT,
        description TEXT,
        seniority TEXT,
        employment_type TEXT,
        function TEXT,
        industry TEXT
    );"""

    curs.execute(sql_command)


    print("Connected to SQLite and table was created")

except sqlite3.Error as error:
    print("Failed to connect with sqlite3 database", error)

finally:
    # Inside Finally Block, If connection is open, we need to close it
    if conn:
        conn.close()
        # using close() method, we will close the connection
        # After closing connection object, we will print "the sqlite connection is closed"
        print("the SQLite connection is closed")
