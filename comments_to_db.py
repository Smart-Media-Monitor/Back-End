import json
import psycopg2
from config import DB_URI


def insert_comments_from_json(json_file, conn):
    with open(json_file, 'r', encoding='utf-8') as jsonfile:
        comments = json.load(jsonfile)

    cur = conn.cursor()
    for comment in comments:
        # Convert 'Likes' and 'Reply_Count' to integers
        try:
            likes = int(float(comment['Likes']))
            reply_count = int(float(comment['Reply Count']))
        except ValueError:
            # Handle invalid values gracefully
            likes = 0
            reply_count = 0
        
        cur.execute("""
            INSERT INTO comments (Name, Comment, Likes, Time, Reply_Count, Label, Label_Score, Video_ID, Comment_Id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            comment['Name'],
            comment['Comment'],
            likes,
            comment['Time'],
            reply_count,
            comment['Label'],
            comment['Label Score'],
            comment['Video ID'],
            comment['Comment Id']
        ))
    conn.commit()
    cur.close()


# Path to the JSON file
json_file = 'comments.json'

# Connect to PostgreSQL using the DB URI
conn = psycopg2.connect(DB_URI)

# Insert data from JSON file into the comments table
insert_comments_from_json(json_file, conn)

# Close the connection
conn.close()
