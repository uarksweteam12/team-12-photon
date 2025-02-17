import psycopg2
import time

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    'password': 'student',
    'host': 'localhost',
    'port': '5432'
}

tryUpdate = False  # Set to True if you want to insert a new player
new_player_id = 501  # Change this as needed
new_codename = "NovaStar"  # Change this as needed

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Execute a query
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"Connected to - {version}")

    # Creating the table (without SERIAL)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id INT PRIMARY KEY,
            player_codename VARCHAR(60) UNIQUE NOT NULL
        );
    ''')

    # Fetch and display existing data
    cursor.execute("SELECT * FROM players;")
    rows = cursor.fetchall()
    print("Current Players in DB:")
    for row in rows:
        print(row)

    def update_database():
        while True:
            if tryUpdate:
                tryUpdate = False  # Reset flag after processing
                if new_player_id and new_codename:
                    print(f"Updating database: ID={new_player_id}, Codename={new_codename}")
                    
                    try:
                        # Insert new player with manually assigned ID
                        cursor.execute('''
                            INSERT INTO players (player_id, player_codename) 
                            VALUES (%s, %s);
                        ''', (new_player_id, new_codename))

                        conn.commit()
                        print(f"New player added successfully: ID={new_player_id}, Codename={new_codename}")

                        # Verify insertion
                        cursor.execute("SELECT * FROM players;")
                        rows = cursor.fetchall()
                        print("Updated Players List:")
                        for row in rows:
                            print(row)

                    except psycopg2.IntegrityError:
                        conn.rollback()
                        print(f"Error: The player ID '{new_player_id}' or codename '{new_codename}' already exists.")
                else:
                    print("Error: Missing player ID or codename")
            time.sleep(0.1)  # Prevent CPU overuse

except Exception as error:
    print(f"Error connecting to PostgreSQL database: {error}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()