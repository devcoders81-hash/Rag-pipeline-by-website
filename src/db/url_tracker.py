import sqlite3

# ----------------------------------------
# Create connection
# ----------------------------------------
conn = sqlite3.connect(
    "url_tracker.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ----------------------------------------
# Create table
# ----------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS ingested_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    status TEXT
)
""")

conn.commit()


# ----------------------------------------
# Check URL exists
# ----------------------------------------
def check_url_exists(url):

    cursor.execute(
        "SELECT * FROM ingested_urls WHERE url=?",
        (url,)
    )

    result = cursor.fetchone()

    return result is not None


# ----------------------------------------
# Insert URL
# ----------------------------------------
def insert_url(url):

    cursor.execute(
        "INSERT INTO ingested_urls (url, status) VALUES (?, ?)",
        (url, "done")
    )

    conn.commit()