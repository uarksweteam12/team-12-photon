import psycopg2
from psycopg2 import sql

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    #'password': 'student',  # Uncomment and provide password if needed
    #'host': 'localhost',    # Uncomment and provide host if needed
    #'port': '5432'          # Uncomment and provide port if needed
}

global conn
global cursor

print("""Connect to PostgreSQL database and return connection and cursor.""")
try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # Execute a query
    cursor.execute("SELECT version();")

    # Fetch and display the result
    version = cursor.fetchone()
    print(f"Connected to - {version}")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id VARCHAR(60),
            name VARCHAR(60)
        );
    ''')

    # Commit the changes
    conn.commit()

except Exception as e:
    print(f"Error connecting to database: {e}")

def insert_player(player_id, codename):
    """Insert a new player into the database."""
    # Connect to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    if conn and cursor:
        try:
            cursor.execute('''INSERT INTO players (id, codename) VALUES (%s, %s);''', (player_id, codename))
            conn.commit()
            print(f"Inserted player {player_id} with codename {codename}")
        except Exception as e:
            print(f"Error inserting player: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

def playerIdExist(playerid):
    """Check to see if playerID exists in database"""
    # Connect to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    print(f"\n\nplayeridexist idvar: {playerid}\n\n")

    if conn and cursor:
        try:
            cursor.execute("SELECT codename FROM players WHERE id = %s;", (str(playerid),))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error checking player id: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")
        return None

def fetch_players():
    """Fetch all players from the database."""
    # Connect to PostgreSQL
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()
    players = []
    if conn and cursor:
        try:
            cursor.execute("SELECT * FROM players;")
            players = cursor.fetchall()
            print("Fetched players from the database:", players)
        except Exception as e:
            print(f"Error fetching players: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")
    return players