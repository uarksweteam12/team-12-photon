import psycopg2
from psycopg2 import sql

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    'password': 'student',  # Uncomment and provide password if needed
    'host': 'localhost',    # Uncomment and provide host if needed
    'port': '5432'          # Uncomment and provide port if needed
}

def connect_to_db():
    """Connect to PostgreSQL database and return connection and cursor."""
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None, None

def insert_player(player_id, codename):
    """Insert a new player into the database."""
    conn, cursor = connect_to_db()
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

def fetch_players():
    """Fetch all players from the database."""
    conn, cursor = connect_to_db()
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
