from googleapiclient.discovery import build
import pandas as pd


def scraper(Api_Key, ID):
    """
    Scrapes YouTube comments and replies for a given video ID using the YouTube Data API.

    Args:
        Api_Key (str): YouTube Data API key for authentication.
        ID (str): YouTube video ID for which comments and replies will be scraped.

    Returns:
        str: JSON representation of the scraped data.
    """
    youtube = build('youtube', 'v3', developerKey=Api_Key)
    result_list = [['Name', 'Comment', 'Likes', 'Time', 'Reply Count']]

    # Initial request to get comments
    data = youtube.commentThreads().list(part='snippet', videoId=ID,
                                         maxResults='100', textFormat="plainText").execute()

    # Extract comments and replies from the initial request
    for item in data["items"]:
        name = item["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
        comment = item["snippet"]['topLevelComment']["snippet"]["textDisplay"]
        likes = item["snippet"]['topLevelComment']["snippet"]['likeCount']
        published_at = item["snippet"]['topLevelComment']["snippet"]['publishedAt']
        replies = item["snippet"]['totalReplyCount']

        result_list.append([name, comment, likes, published_at, replies])

        total_reply_count = item["snippet"]['totalReplyCount']

        # If there are replies, fetch them
        if total_reply_count > 0:
            parent_comment_id = item["snippet"]['topLevelComment']["id"]
            replies_data = youtube.comments().list(part='snippet', maxResults='100', parentId=parent_comment_id,
                                                   textFormat="plainText").execute()

            # Extract replies data
            for reply_item in replies_data["items"]:
                name = reply_item["snippet"]["authorDisplayName"]
                reply_comment = reply_item["snippet"]["textDisplay"]
                reply_likes = reply_item["snippet"]['likeCount']
                reply_published_at = reply_item["snippet"]['publishedAt']

                result_list.append(
                    [name, reply_comment, reply_likes, reply_published_at, ''])

    # Continue fetching comments from the next pages, if available
    while "nextPageToken" in data:
        data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                             maxResults='100', textFormat="plainText").execute()

        for item in data["items"]:
            name = item["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = item["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            likes = item["snippet"]['topLevelComment']["snippet"]['likeCount']
            published_at = item["snippet"]['topLevelComment']["snippet"]['publishedAt']
            replies = item["snippet"]['totalReplyCount']

            result_list.append([name, comment, likes, published_at, replies])

            total_reply_count = item["snippet"]['totalReplyCount']

            # If there are replies, fetch them
            if total_reply_count > 0:
                parent_comment_id = item["snippet"]['topLevelComment']["id"]
                replies_data = youtube.comments().list(part='snippet', maxResults='100', parentId=parent_comment_id,
                                                       textFormat="plainText").execute()

                # Extract replies data
                for reply_item in replies_data["items"]:
                    name = reply_item["snippet"]["authorDisplayName"]
                    reply_comment = reply_item["snippet"]["textDisplay"]
                    reply_likes = reply_item["snippet"]['likeCount']
                    reply_published_at = reply_item["snippet"]['publishedAt']

                    result_list.append(
                        [name, reply_comment, reply_likes, reply_published_at, ''])

    # Create a DataFrame from the result list
    df = pd.DataFrame({'Name': [i[0] for i in result_list],
                       'Comment': [i[1] for i in result_list],
                       'Likes': [i[2] for i in result_list],
                       'Time': [i[3] for i in result_list],
                       'Reply Count': [i[4] for i in result_list]})

    # Save DataFrame to CSV
    df.to_csv('YT-Scrape-Result.csv', index=False, header=False)

    # Return JSON representation of the DataFrame
    return df.to_json()


Api_Key = "AIzaSyBNBl0sWSbRIKpp_I0jNpWIzMarOdhYM90"
ID = "8mjcnxGMwFo"

scraper(Api_Key, ID)
