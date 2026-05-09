import sqlite3


# ---------------------------------------------------
# Global Variables (Singleton Pattern)
# ---------------------------------------------------
conn = None


# ---------------------------------------------------
# Get SQLite Connection (Load Only Once)
# ---------------------------------------------------
def get_connection():

    global conn

    if conn is None:

        print("Loading SQLite connection...")

        conn = sqlite3.connect(
            "url_tracker.db",
            check_same_thread=False
        )

    return conn


# ---------------------------------------------------
# Initialize Database
# ---------------------------------------------------
def init_db():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingested_urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE,
        status TEXT
    )
    """)

    connection.commit()

    print("SQLite initialized successfully")


# ---------------------------------------------------
# Check URL Exists
# ---------------------------------------------------
def check_url_exists(url):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM ingested_urls WHERE url=?",
        (url,)
    )

    result = cursor.fetchone()

    return result is not None


# ---------------------------------------------------
# Insert URL
# ---------------------------------------------------
def insert_url(url):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO ingested_urls (url, status) VALUES (?, ?)",
        (url, "done")
    )

    connection.commit()

    print("URL inserted successfully")


# ---------------------------------------------------
# Optional Close Connection
# ---------------------------------------------------
def close_connection():

    global conn

    if conn is not None:

        conn.close()

        conn = None

        print("SQLite connection closed")