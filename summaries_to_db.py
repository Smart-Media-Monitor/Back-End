import json
import psycopg2
from config import DB_URI


def insert_summaries_from_json(json_file, conn):
    with open(json_file, 'r', encoding='utf-8') as jsonfile:
        summaries = json.load(jsonfile)

    cur = conn.cursor()
    for summary in summaries:
        cur.execute("""
            INSERT INTO summaries (Label, Summary)
            VALUES (%s, %s)
        """, (
            summary['Label'],
            summary['Summary']
        ))
    conn.commit()
    cur.close()


# Path to the JSON file
json_file = 'summaries.json'

# Connect to PostgreSQL using the DB URI
conn = psycopg2.connect(DB_URI)

# Insert data from JSON file into the summaries table
insert_summaries_from_json(json_file, conn)

# Close the connection
conn.close()
