import googleapiclient.discovery
import sys

def get_channel_info(api_key, channel_ids):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    channel_info_list = []

    for channel_id in channel_ids:
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )

        response = request.execute()

        if 'items' in response and response['items']:
            channel_data = response['items'][0]

            channel_info = {
                "channel_id": channel_data["id"],
                "channel_name": channel_data["snippet"]["title"],
                "subscribers": int(channel_data["statistics"]["subscriberCount"]),
                "views": int(channel_data["statistics"]["viewCount"]),
                "total_videos": int(channel_data["statistics"]["videoCount"]),
                "channel_description": channel_data["snippet"]["description"],
                "playlist_id": channel_data["contentDetails"]["relatedPlaylists"]["uploads"]
            }

            channel_info_list.append(channel_info)

    return channel_info_list

# Example usage
channel_ids = [
    "UCuI5XcJYynHa5k_lqDzAgwQ",
    "UCnz-ZXXER4jOvuED5trXfEA",
    "UCPMkWVHlZAAmqm0-UHLpO5w",
    "UCbUvh29BX2Db8sGJOOszyXA",
    "UCYpfpuS8yvd31i1_CC3SvBQ",
    "UCX4vsVEPB0V9EX8EODR0R-w",
    "UCsQJVg9nfOuqMYt42c3nPaA",
    "UCOe3UfwbrwmGp99O4ukWPhA",
    "UCKulbtdZOJB9sWxLePjh2xA",
    "UCRht8PDFgMhyIEXRpF7DHSA"
]

api_key = "AIzaSyB79fCrb-8K38Bwq-2CA8e1vY7D8kBy8H8"

channel_info_list = get_channel_info(api_key, channel_ids)

# Print the results with channel_name included
for channel_info in channel_info_list:
    print("Channel Name:", channel_info["channel_name"])
    print("Channel ID:", channel_info["channel_id"])
    print("Subscribers:", channel_info["subscribers"])
    print("Views:", channel_info["views"])
    print("Total Videos:", channel_info["total_videos"])
    print("Description:", channel_info["channel_description"].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
    print("Playlist ID:", channel_info["playlist_id"])
    print("-----------------------------")
###########################################################################################################################################################
import googleapiclient.discovery

def get_video_IDs(api_key, channel_ids):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    all_video_ids = []

    for channel_id in channel_ids:
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )

        response = request.execute()

        if 'items' in response and response['items']:
            uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            # Get videos from the uploads playlist
            playlist_request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50  # Adjust as needed
            )

            playlist_response = playlist_request.execute()

            # Extract video IDs
            video_ids = [item['contentDetails']['videoId'] for item in playlist_response.get('items', [])]

            all_video_ids.extend(video_ids)

    return all_video_ids

# Example usage
channel_ids = [
    "UCuI5XcJYynHa5k_lqDzAgwQ",
    "UCnz-ZXXER4jOvuED5trXfEA",
    "UCPMkWVHlZAAmqm0-UHLpO5w",
    "UCbUvh29BX2Db8sGJOOszyXA",
    "UCYpfpuS8yvd31i1_CC3SvBQ",
    "UCX4vsVEPB0V9EX8EODR0R-w",
    "UCsQJVg9nfOuqMYt42c3nPaA",
    "UCOe3UfwbrwmGp99O4ukWPhA",
    "UCKulbtdZOJB9sWxLePjh2xA",
    "UCRht8PDFgMhyIEXRpF7DHSA"
]

api_key = "AIzaSyB79fCrb-8K38Bwq-2CA8e1vY7D8kBy8H8"

video_ids = get_video_IDs(api_key, channel_ids)

# Print the results
print(video_ids)
######################################################################################################################################
import googleapiclient.discovery
import sys

def get_video_IDs(api_key, channel_ids):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    all_video_ids = []

    for channel_id in channel_ids:
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )

        response = request.execute()

        if 'items' in response and response['items']:
            uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            # Get videos from the uploads playlist
            playlist_request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50  # Adjust as needed
            )

            playlist_response = playlist_request.execute()

            # Extract video IDs
            video_ids = [item['contentDetails']['videoId'] for item in playlist_response.get('items', [])]

            all_video_ids.extend(video_ids)

    return all_video_ids

def get_video_info(api_key, video_ids):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    all_video_info = []

    for video_id in video_ids:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )

        response = request.execute()

        if 'items' in response and response['items']:
            video_data = response['items'][0]

            video_info = {
                "channel_name": video_data["snippet"]["channelTitle"],
                "channel_id": video_data["snippet"]["channelId"],
                "video_id": video_id,
                "title": video_data["snippet"]["title"].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding),
                "tags": [tag.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding) for tag in video_data["snippet"].get("tags", [])],
                "thumbnail": video_data["snippet"]["thumbnails"]["default"]["url"],
                "description": video_data["snippet"]["description"].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding),
                "published_date": video_data["snippet"]["publishedAt"],
                "duration": video_data["contentDetails"]["duration"],
                "views": int(video_data["statistics"]["viewCount"]),
                "likes": int(video_data["statistics"].get("likeCount", 0)),  # Added likes
                "comments": int(video_data["statistics"]["commentCount"]),
                "favorite_count": int(video_data["statistics"]["favoriteCount"]),
                "definition": video_data["contentDetails"]["definition"],
                "caption_status": video_data["contentDetails"]["caption"]
            }

            all_video_info.append(video_info)

    return all_video_info

# Example usage
channel_ids = [
    "UCuI5XcJYynHa5k_lqDzAgwQ",
    "UCnz-ZXXER4jOvuED5trXfEA",
    "UCPMkWVHlZAAmqm0-UHLpO5w",
    "UCbUvh29BX2Db8sGJOOszyXA",
    "UCYpfpuS8yvd31i1_CC3SvBQ",
    "UCX4vsVEPB0V9EX8EODR0R-w",
    "UCsQJVg9nfOuqMYt42c3nPaA",
    "UCOe3UfwbrwmGp99O4ukWPhA",
    "UCKulbtdZOJB9sWxLePjh2xA",
    "UCRht8PDFgMhyIEXRpF7DHSA"
]

api_key = "AIzaSyB79fCrb-8K38Bwq-2CA8e1vY7D8kBy8H8"

video_ids = get_video_IDs(api_key, channel_ids)
video_info_list = get_video_info(api_key, video_ids)

# Print the results
for video_info in video_info_list:
    print("Channel Name:", video_info["channel_name"])
    print("Channel ID:", video_info["channel_id"])
    print("Video ID:", video_info["video_id"])
    print("Title:", video_info["title"])
    print("Tags:", ", ".join(video_info["tags"]))
    print("Thumbnail:", video_info["thumbnail"])
    print("Description:", video_info["description"])
    print("Published Date:", video_info["published_date"])
    print("Duration:", video_info["duration"])
    print("Views:", video_info["views"])
    print("Likes:", video_info["likes"])  # Include likes
    print("Comments:", video_info["comments"])
    print("Favorite Count:", video_info["favorite_count"])
    print("Definition:", video_info["definition"])
    print("Caption Status:", video_info["caption_status"])
    print("-----------------------------")


############################################################################################################################################
import googleapiclient.discovery
import sys

def get_comment_info(api_key, video_ids):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    all_comment_info = []

    for video_id in video_ids:
        try:
            request = youtube.commentThreads().list(
                part="id,snippet",
                videoId=video_id,
                textFormat="plainText"
            )

            response = request.execute()

            if 'items' in response:
                for comment_thread in response['items']:
                    comment_data = comment_thread['snippet']['topLevelComment']['snippet']

                    comment_info = {
                        "comment_id": comment_thread['id'],
                        "video_id": video_id,
                        "comment_text": comment_data['textDisplay'].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding),
                        "comment_author": comment_data['authorDisplayName'],
                        "comment_published": comment_data['publishedAt']
                    }

                    all_comment_info.append(comment_info)

        except googleapiclient.errors.HttpError as e:
            # Handle 403 Forbidden (commentsDisabled) error
            if e.resp.status == 403:
                print(f"Comments are disabled for the video with ID {video_id}. Skipping.")
            else:
                raise  # Re-raise other HTTP errors

    return all_comment_info

# Example usage
channel_ids = [
    "UCuI5XcJYynHa5k_lqDzAgwQ",
    "UCnz-ZXXER4jOvuED5trXfEA",
    "UCPMkWVHlZAAmqm0-UHLpO5w",
    "UCbUvh29BX2Db8sGJOOszyXA",
    "UCYpfpuS8yvd31i1_CC3SvBQ",
    "UCX4vsVEPB0V9EX8EODR0R-w",
    "UCsQJVg9nfOuqMYt42c3nPaA",
    "UCOe3UfwbrwmGp99O4ukWPhA",
    "UCKulbtdZOJB9sWxLePjh2xA",
    "UCRht8PDFgMhyIEXRpF7DHSA"
]

api_key = "AIzaSyB79fCrb-8K38Bwq-2CA8e1vY7D8kBy8H8"

video_ids = get_video_IDs(api_key, channel_ids)
comment_info_list = get_comment_info(api_key, video_ids)

# Print the results
for comment_info in comment_info_list:
    print("Comment ID:", comment_info["comment_id"])
    print("Video ID:", comment_info["video_id"])
    print("Comment Text:", comment_info["comment_text"])
    print("Comment Author:", comment_info["comment_author"])
    print("Comment Published:", comment_info["comment_published"])
    print("-----------------------------")
#########################################################################################################################
import googleapiclient.discovery
import sys

def get_playlist_details(api_key, channel_ids):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    all_playlist_details = []

    for channel_id in channel_ids:
        request = youtube.playlists().list(
            part="id,snippet,contentDetails",
            channelId=channel_id,
            maxResults=50  # Adjust as needed
        )

        response = request.execute()

        if 'items' in response:
            for playlist_data in response['items']:
                snippet = playlist_data['snippet']
                content_details = playlist_data['contentDetails']

                playlist_details = {
                    "playlist_id": playlist_data['id'],
                    "title": snippet['title'].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding),
                    "channel_id": channel_id,
                    "channel_name": snippet['channelTitle'],
                    "published_at": snippet['publishedAt'],
                    "video_count": content_details['itemCount']
                }

                all_playlist_details.append(playlist_details)

    return all_playlist_details

# Example usage
channel_ids = [
    "UCuI5XcJYynHa5k_lqDzAgwQ",
    "UCnz-ZXXER4jOvuED5trXfEA",
    "UCPMkWVHlZAAmqm0-UHLpO5w",
    "UCbUvh29BX2Db8sGJOOszyXA",
    "UCYpfpuS8yvd31i1_CC3SvBQ",
    "UCX4vsVEPB0V9EX8EODR0R-w",
    "UCsQJVg9nfOuqMYt42c3nPaA",
    "UCOe3UfwbrwmGp99O4ukWPhA",
    "UCKulbtdZOJB9sWxLePjh2xA",
    "UCRht8PDFgMhyIEXRpF7DHSA"
]

api_key = "AIzaSyB79fCrb-8K38Bwq-2CA8e1vY7D8kBy8H8"

playlist_details_list = get_playlist_details(api_key, channel_ids)

# Print the results
for playlist_details in playlist_details_list:
    print("Playlist ID:", playlist_details["playlist_id"])
    print("Title:", playlist_details["title"])
    print("Channel ID:", playlist_details["channel_id"])
    print("Channel Name:", playlist_details["channel_name"])
    print("Published At:", playlist_details["published_at"])
    print("Video Count:", playlist_details["video_count"])
    print("-----------------------------")
######################################################################################################################################
import googleapiclient.discovery
import urllib.parse
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId from bson

# (Your existing functions)

# Check if data already exists in MongoDB
def is_data_exists(collection, query):
    return collection.find_one(query) is not None

# Insert data into MongoDB only if it doesn't exist
def insert_data_if_not_exists(collection, data_list):
    for data in data_list:
        doc_id = data.get("_id")
        if not doc_id:
            # If "_id" is missing, generate a new ObjectId
            data["_id"] = ObjectId()

        if not is_data_exists(collection, {"_id": data["_id"]}):
            collection.insert_one(data)
            print(f"Inserted: {data}")
        else:
            print(f"Already exists: {data}")

# Example usage
api_key = "AIzaSyB79fCrb-8K38Bwq-2CA8e1vY7D8kBy8H8"
channel_ids = [
    "UCuI5XcJYynHa5k_lqDzAgwQ",
    "UCnz-ZXXER4jOvuED5trXfEA",
    "UCPMkWVHlZAAmqm0-UHLpO5w",
    "UCbUvh29BX2Db8sGJOOszyXA",
    "UCYpfpuS8yvd31i1_CC3SvBQ",
    "UCX4vsVEPB0V9EX8EODR0R-w",
    "UCsQJVg9nfOuqMYt42c3nPaA",
    "UCOe3UfwbrwmGp99O4ukWPhA",
    "UCKulbtdZOJB9sWxLePjh2xA",
    "UCRht8PDFgMhyIEXRpF7DHSA"
]

# (Your existing data retrieval code)

# Connection details
username = "arafathyasar418"
password = "Yasar@007"
database_name = "youtube_project"

# Escape the username and password
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Construct the MongoDB Atlas URI
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.a10y7ox.mongodb.net/{database_name}?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(uri)

# Access the specified database and collections
db = client.get_database(database_name)

# Insert data into MongoDB
insert_data_if_not_exists(db.get_collection("channel_information"), channel_info_list)
insert_data_if_not_exists(db.get_collection("video_information"), video_info_list)
insert_data_if_not_exists(db.get_collection("comment_information"), comment_info_list)
insert_data_if_not_exists(db.get_collection("playlist_information"), playlist_details_list)
######################################################################################################################################################
import pandas as pd
import sqlite3
from pymongo import MongoClient
import urllib.parse

# MongoDB Connection
username = "arafathyasar418"
password = "Yasar@007"
database_name = "youtube_project"
collection_name = "channel_information"

escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Construct the MongoDB Atlas URI
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.a10y7ox.mongodb.net/{database_name}?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(uri)

# Access the specified collection
collection = client.get_database(database_name).get_collection(collection_name)

# Retrieve data from MongoDB and convert to DataFrame
mongo_data = list(collection.find())
df = pd.DataFrame(mongo_data, columns=['channel_id', 'channel_name', 'subscribers', 'views', 'total_videos', 'channel_description', 'playlist_id'])

# Drop duplicate rows based on 'channel_id'
df.drop_duplicates(subset=['channel_id'], keep='first', inplace=True)

# SQLite Connection
conn = sqlite3.connect('your_database.db')

# SQL Query to create the table
create_table_query = '''
    CREATE TABLE IF NOT EXISTS channel_table (
        channel_id VARCHAR(80) PRIMARY KEY,
        channel_name VARCHAR(80),
        subscribers BIGINT,
        views BIGINT,
        total_videos INT,
        channel_description TEXT,
        playlist_id VARCHAR(80)
    );
'''

# Execute the create table query
conn.execute(create_table_query)

# SQL Query to insert data into the table
insert_query = '''
    INSERT OR REPLACE INTO channel_table
    (channel_id, channel_name, subscribers, views, total_videos, channel_description, playlist_id)
    VALUES (?, ?, ?, ?, ?, ?, ?);
'''

# Execute the insert query with data from the DataFrame
conn.executemany(insert_query, df.values)

# Commit changes and close the connection
conn.commit()
conn.close()

# Display the modified DataFrame
print(df)
################################################################################################################################################
import pandas as pd
import sqlite3
from pymongo import MongoClient
import urllib.parse

# MongoDB Connection
username = "arafathyasar418"
password = "Yasar@007"
database_name = "youtube_project"
collection_name_playlist = "playlist_information"

escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Construct the MongoDB Atlas URI
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.a10y7ox.mongodb.net/{database_name}?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(uri)

# Access the specified collection for playlist information
collection_playlist = client.get_database(database_name).get_collection(collection_name_playlist)

# Retrieve data from MongoDB and convert to DataFrame for playlist information
mongo_data_playlist = list(collection_playlist.find())
df_playlist = pd.DataFrame(mongo_data_playlist, columns=['playlist_id', 'title', 'channel_id', 'channel_name', 'published_at', 'video_count'])

# Drop duplicate rows based on 'playlist_id'
df_playlist.drop_duplicates(subset=['playlist_id'], keep='first', inplace=True)

# SQLite Connection
conn = sqlite3.connect('your_database.db')

# SQL Query to create the playlist table
create_playlist_table_query = '''
    CREATE TABLE IF NOT EXISTS playlist_table (
        playlist_id VARCHAR(100) PRIMARY KEY,
        title VARCHAR(100),
        channel_id VARCHAR(100),
        channel_name VARCHAR(100),
        published_at TIMESTAMP,
        video_count INT
    );
'''

# Execute the create table query for the playlist
conn.execute(create_playlist_table_query)

# SQL Query to insert data into the playlist table
insert_playlist_query = '''
    INSERT OR REPLACE INTO playlist_table
    (playlist_id, title, channel_id, channel_name, published_at, video_count)
    VALUES (?, ?, ?, ?, ?, ?);
'''

# Execute the insert query with data from the playlist DataFrame
conn.executemany(insert_playlist_query, df_playlist.values)

# Commit changes and close the connection
conn.commit()
conn.close()

# Display the modified playlist DataFrame
print(df_playlist)
##############################################################################################################################################
import pandas as pd
import sqlite3
from pymongo import MongoClient
import urllib.parse

# MongoDB Connection
username = "arafathyasar418"
password = "Yasar@007"
database_name = "youtube_project"
collection_name_comment = "comment_information"

escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Construct the MongoDB Atlas URI
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.a10y7ox.mongodb.net/{database_name}?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(uri)

# Access the specified collection for comment information
collection_comment = client.get_database(database_name).get_collection(collection_name_comment)

# Retrieve data from MongoDB and convert to DataFrame for comment information
mongo_data_comment = list(collection_comment.find())
df_comment = pd.DataFrame(mongo_data_comment, columns=['comment_id', 'video_id', 'comment_text', 'comment_author', 'comment_published'])

# Drop duplicate rows based on 'comment_id'
df_comment.drop_duplicates(subset=['comment_id'], keep='first', inplace=True)

# SQLite Connection
conn = sqlite3.connect('your_database.db')

# SQL Query to create the comment table
create_comment_table_query = '''
    CREATE TABLE IF NOT EXISTS comment_table (
        comment_id VARCHAR(100) PRIMARY KEY,
        video_id VARCHAR(100),
        comment_text TEXT,
        comment_author VARCHAR(100),
        comment_published TIMESTAMP
    );
'''

# Execute the create table query for the comment table
conn.execute(create_comment_table_query)

# SQL Query to insert data into the comment table
insert_comment_query = '''
    INSERT OR REPLACE INTO comment_table
    (comment_id, video_id, comment_text, comment_author, comment_published)
    VALUES (?, ?, ?, ?, ?);
'''

# Execute the insert query with data from the comment DataFrame
conn.executemany(insert_comment_query, df_comment.values)

# Commit changes and close the connection
conn.commit()
conn.close()

# Display the modified comment DataFrame
print(df_comment)
#####################################################################################################################################
import pandas as pd
import sqlite3
from pymongo import MongoClient
import urllib.parse
from isodate import parse_duration

# MongoDB Connection
username = "arafathyasar418"
password = "Yasar@007"
database_name = "youtube_project"
collection_name_video = "video_information"

escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Construct the MongoDB Atlas URI
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.a10y7ox.mongodb.net/{database_name}?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(uri)

# Access the specified collection for video information
collection_video = client.get_database(database_name).get_collection(collection_name_video)

# Retrieve data from MongoDB and convert to DataFrame for video information
mongo_data_video = list(collection_video.find())
df_video = pd.DataFrame(mongo_data_video, columns=['channel_name', 'channel_id', 'video_id', 'title', 'tags', 'thumbnail', 'description', 'published_date', 'duration', 'views', 'likes', 'comments', 'favorite_count', 'definition', 'caption_status'])

# Drop duplicate rows based on 'video_id'
df_video.drop_duplicates(subset=['video_id'], keep='first', inplace=True)

# Convert 'duration' to total seconds (integer)
df_video['duration_seconds'] = df_video['duration'].apply(lambda x: int(parse_duration(x).total_seconds()))

# Convert 'tags' to a string
df_video['tags'] = df_video['tags'].astype(str)

# SQLite Connection
conn = sqlite3.connect('your_database.db')

# SQL Query to create the video table
create_video_table_query = '''
    CREATE TABLE IF NOT EXISTS video_table (
        channel_name VARCHAR(100),
        channel_id VARCHAR(100),
        video_id VARCHAR(30) PRIMARY KEY,
        title VARCHAR(150),
        tags TEXT,
        thumbnail VARCHAR(200),
        description TEXT,
        published_date TIMESTAMP,
        duration INTEGER,
        views BIGINT,
        likes BIGINT,
        comments INT,
        favorite_count INT,
        definition VARCHAR(10),
        caption_status VARCHAR(50)
    );
'''

# Execute the create table query for the video table
conn.execute(create_video_table_query)

# Loop through each row and insert data into the video table
for index, row in df_video.iterrows():
    # Convert 'duration' to total seconds (integer)
    row['duration_seconds'] = int(parse_duration(row['duration']).total_seconds())
    # Convert 'tags' to a string
    row['tags'] = str(row['tags'])
    # Execute the insert query for the current row
    conn.execute('''
        INSERT OR REPLACE INTO video_table
        (channel_name, channel_id, video_id, title, tags, thumbnail, description, published_date, duration, views, likes, comments, favorite_count, definition, caption_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (row['channel_name'], row['channel_id'], row['video_id'], row['title'], row['tags'], row['thumbnail'], row['description'], row['published_date'], row['duration_seconds'], row['views'], row['likes'], row['comments'], row['favorite_count'], row['definition'], row['caption_status']))

# Commit changes and close the connection
conn.commit()
conn.close()

# Display the modified video DataFrame
print(df_video)
####################################################################################################################################
import streamlit as st

# Set page title
st.set_page_config(page_title="YouTube Data Dashboard", page_icon="📊", layout="wide")

# Sidebar with custom styling
st.sidebar.markdown(
    """
    <style>
        .sidebar-title {
            font-size: 18px;
            font-weight: bold;
            color: red;
            text-transform: uppercase;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar title
st.sidebar.markdown('<p class="sidebar-title">YOUTUBE DATA HARVESTING AND WAREHOUSING</p>', unsafe_allow_html=True)

# Main content area
st.title("Skills Takeaway")
st.markdown("## Python Scripting")
st.markdown("## Data Collection")
st.markdown("## MongoDB")
st.markdown("## API Integration")
st.markdown("## Data Management using MongoDB and SQL")

# Custom styling for header
st.markdown(
    """
    <style>
        .header {
            color: blue;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<p class="header">Skills Takeaway</p>', unsafe_allow_html=True)
#######################################################################################################################
import streamlit as st
import pandas as pd
import sqlite3
from pymongo import MongoClient
from bson import ObjectId
from isodate import parse_duration

# MongoDB Connection
def connect_to_mongodb():
    username = "arafathyasar418"
    password = "Yasar@007"
    database_name = "youtube_project"
    escaped_username = urllib.parse.quote_plus(username)
    escaped_password = urllib.parse.quote_plus(password)
    uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.a10y7ox.mongodb.net/{database_name}?retryWrites=true&w=majority"
    client = MongoClient(uri)
    return client.get_database(database_name)

# SQLite Connection
def connect_to_sqlite():
    conn = sqlite3.connect('your_database.db')
    return conn

# Function to collect and store data in MongoDB
def collect_and_store_data(channel_id, mongodb_collection):
    # Your data retrieval and insertion logic here based on the given channel_id
    # For example, let's assume you have a function retrieve_data_from_api(channel_id) to get data
    # data_to_insert = retrieve_data_from_api(channel_id)

    # Insert data into MongoDB
    # mongodb_collection.insert_one(data_to_insert)

    # Simulate data insertion for demonstration purposes
    data_to_insert = {
        "_id": ObjectId(),
        "channel_id": channel_id,
        "example_data": "Some data",
    }
    mongodb_collection.insert_one(data_to_insert)
    return data_to_insert

# Function to migrate data to SQLite
def migrate_to_sqlite(data_to_migrate, sqlite_connection):
    # Your migration logic here
    # For example, assume you have a function insert_data_into_sqlite(data, sqlite_connection) to insert data
    # insert_data_into_sqlite(data_to_migrate, sqlite_connection)

    # Simulate migration for demonstration purposes
    sqlite_connection.execute('''
        INSERT OR REPLACE INTO migrated_data_table
        (channel_id, example_data)
        VALUES (?, ?)
    ''', (data_to_migrate["channel_id"], data_to_migrate["example_data"]))

# Streamlit App
st.title("YouTube Data Collection and Migration")
channel_id_input = st.text_input("Enter the Channel ID:")
button_collect = st.button("Collect and Store Data")

if button_collect:
    if not channel_id_input:
        st.warning("Please enter a Channel ID.")
    else:
        # Connect to MongoDB
        mongodb_collection = connect_to_mongodb().get_collection("channel_information")

        # Check if data already exists in MongoDB
        if is_data_exists(mongodb_collection, {"channel_id": channel_id_input}):
            st.warning("Channel ID already exists in MongoDB. Data not collected.")
        else:
            # Collect and store data in MongoDB
            collected_data = collect_and_store_data(channel_id_input, mongodb_collection)
            st.success("Data collected and stored in MongoDB.")
            st.write("Collected Data:")
            st.write(collected_data)

# Button to migrate data to SQLite
button_migrate_to_sql = st.button("Migrate to SQL")

if button_migrate_to_sql:
    if not channel_id_input:
        st.warning("Please enter a Channel ID.")
    else:
        # Connect to SQLite
        sqlite_connection = connect_to_sqlite()

        # Retrieve data from MongoDB
        data_to_migrate = mongodb_collection.find_one({"channel_id": channel_id_input})

        if data_to_migrate:
            # Migrate data to SQLite
            migrate_to_sqlite(data_to_migrate, sqlite_connection)
            st.success("Data successfully migrated to SQLite.")
        else:
            st.warning("No data found for the given Channel ID in MongoDB.")

# Display the SQLite table if it exists
if sqlite_connection:
    df_sqlite = pd.read_sql_query("SELECT * FROM migrated_data_table", sqlite_connection)
    st.write("SQLite Table:")
    st.write(df_sqlite)

# Close SQLite connection
if sqlite_connection:
    sqlite_connection.close()