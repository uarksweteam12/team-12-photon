import psycopg2
from psycopg2 import sql

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    #'password': 'student', # Uncomment and provide password if needed
    #'host': 'localhost',   # Uncomment and provide host if needed
    #'port': '5432'         # Uncomment and provide port if needed
}

cursor = None
conn = None

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Execute a query
    cursor.execute("SELECT version();")

    # Fetch and display the result
    version = cursor.fetchone()
    print(f"Connected to - {version}")

    # Create the players table
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS players (
           id INT PRIMARY KEY,
           codename VARCHAR(60) UNIQUE NOT NULL
       );
    ''')

    # Insert sample data
    cursor.execute('''
        INSERT INTO players (id, codename)
        VALUES (%s, %s);
    ''', (500, 'BhodiLi'))

    # Commit the changes
    conn.commit()

    # Fetch and display data from the table
    cursor.execute("SELECT * FROM players;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Exception as error:
    print(f"Error connecting to PostgreSQL database: {error}")

finally:
    # Close the cursor and connection if they were created
    if cursor:
        cursor.close()
    if conn:
        conn.close()
