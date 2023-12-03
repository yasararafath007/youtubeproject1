import streamlit as st
import pandas as pd
import sqlite3
from pymongo import MongoClient
from bson import ObjectId
import urllib.parse

# Initialize mongodb_collection using Streamlit session state
if "mongodb_collection" not in st.session_state:
    st.session_state.mongodb_collection = None

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

# Function to check if data already exists in MongoDB
def is_data_exists(collection, query):
    return collection.find_one(query) is not None

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
def migrate_to_sqlite(channel_id, mongodb_collection, sqlite_connection):
    # Retrieve data from MongoDB based on the Channel ID
    data_to_migrate = mongodb_collection.find_one({"channel_id": channel_id})

    if data_to_migrate:
        # Your migration logic here
        # For example, assume you have a function insert_data_into_sqlite(data, sqlite_connection) to insert data
        # insert_data_into_sqlite(data_to_migrate, sqlite_connection)

        # Simulate migration for demonstration purposes
        sqlite_connection.execute('''
            CREATE TABLE IF NOT EXISTS migrated_data_table (
                channel_id VARCHAR(100) PRIMARY KEY,
                example_data TEXT
            );
        ''')
        sqlite_connection.execute('''
            INSERT OR REPLACE INTO migrated_data_table
            (channel_id, example_data)
            VALUES (?, ?)
        ''', (data_to_migrate["channel_id"], data_to_migrate["example_data"]))

        st.success("Table created successfully.")
    else:
        st.warning("No data found for the given Channel ID in MongoDB.")

# Streamlit App
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
            margin-bottom: 20px;
        }
        .sidebar-captions {
            font-size: 14px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar title
st.sidebar.markdown('<p class="sidebar-title">YOUTUBE DATA HARVESTING AND WAREHOUSING</p>', unsafe_allow_html=True)

# Sidebar captions
st.sidebar.markdown('<p class="sidebar-captions">Skills Takeaway:</p>', unsafe_allow_html=True)
st.sidebar.markdown('- Python Scripting')
st.sidebar.markdown('- Data Collection')
st.sidebar.markdown('- MongoDB')
st.sidebar.markdown('- API Integration')
st.sidebar.markdown('- Data Management using MongoDB and SQL')

channel_id_input = st.text_input("Enter the Channel ID:")
button_collect = st.button("Collect and Store Data")

sqlite_connection = None  # Initialize sqlite_connection

if button_collect:
    if not channel_id_input:
        st.warning("Please enter a Channel ID.")
    else:
        # Connect to MongoDB
        st.session_state.mongodb_collection = connect_to_mongodb().get_collection("channel_information")

        # Check if data already exists in MongoDB
        if is_data_exists(st.session_state.mongodb_collection, {"channel_id": channel_id_input}):
            st.warning("Channel ID already exists in MongoDB. Data not collected.")
        else:
            # Collect and store data in MongoDB
            collected_data = collect_and_store_data(channel_id_input, st.session_state.mongodb_collection)
            st.success("Data collected and stored in MongoDB.")
            st.write("Collected Data:")
            st.write(collected_data)

# Button to migrate data to SQLite
button_migrate_to_sql = st.button("Migrate to SQL")

if button_migrate_to_sql:
    if not channel_id_input:
        st.warning("Please enter a Channel ID.")
    else:
        # Check if mongodb_collection is initialized
        if st.session_state.mongodb_collection is None:
            st.warning("Please collect and store data in MongoDB first.")
        else:
            # Connect to SQLite
            sqlite_connection = connect_to_sqlite()

            # Migrate data to SQLite
            migrate_to_sqlite(channel_id_input, st.session_state.mongodb_collection, sqlite_connection)
# SQLite Connection
sqlite_connection = sqlite3.connect('your_database.db')

# ...

# Radio button to select table
selected_table = st.radio("Select Table:", ["channel_table", "comment_table", "playlist_table", "video_table"])

# Function to retrieve data from SQLite based on the selected table
def retrieve_data_from_sqlite(selected_table, sqlite_connection):
    query = f"SELECT * FROM {selected_table};"
    with sqlite_connection:
        df = pd.read_sql_query(query, sqlite_connection)
    return df

# Display selected table data
st.write(f"Displaying data for {selected_table}:")
table_data = retrieve_data_from_sqlite(selected_table, sqlite_connection)
st.write(table_data)
####################################################################################################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 1: What are the names of all the videos and their corresponding channels?": "SELECT video_id, title, channel_name FROM video_table;",
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
if st.button("Generate Output"):
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])
        
        # Keep only 'title' and 'channel_name' columns
        df_subset = df[['title', 'channel_name']]

        st.write(df_subset)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()
###########################################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 2: Which channels have the most number of videos, and how many videos do they have?":
    "SELECT channel_name, total_videos FROM channel_table ORDER BY total_videos DESC LIMIT 10;"
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
button_clicked = st.button("Generate Output", key="generate_output_button")
if button_clicked:
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])

        st.write(df)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()
###################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 3: What are the top 10 most viewed videos and their respective channels?":
    "SELECT title, channel_name, views FROM video_table ORDER BY views DESC LIMIT 10;"
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
button_clicked = st.button("Generate Output - Question 3", key="generate_output_button_question_3")
if button_clicked:
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])

        st.write(df)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()
#############################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 4: How many comments were made on each video, and what are their corresponding video names?":
    "SELECT video_id, title, comments FROM video_table;"
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
button_clicked = st.button("Generate Output", key=f"generate_output_button_{selected_question}")
if button_clicked:
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])

        st.write(df)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()
###########################################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 5: Which videos have the highest number of likes, and what are their corresponding channel names?":
    """
    SELECT v.video_id, v.title, v.likes, v.channel_name
    FROM video_table v
    JOIN (
        SELECT video_id, MAX(likes) AS max_likes
        FROM video_table
        GROUP BY video_id
    ) t ON v.video_id = t.video_id AND v.likes = t.max_likes
    ORDER BY v.likes DESC;
    """
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
button_clicked = st.button("Generate Output", key="generate_output_button_5")
if button_clicked:
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])

        st.write(df)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()
################################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 6: What is the total number of likes for each video, and what are their corresponding video names?":
    """
    SELECT video_id, title, SUM(likes) AS total_likes
    FROM video_table
    GROUP BY video_id, title;
    """
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
button_clicked = st.button("Generate Output", key="generate_output_button_6")
if button_clicked:
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])

        st.write(df)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()
################################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 7: What is the total number of views for each channel, and what are their corresponding channel names?":
    """
    SELECT channel_id, channel_name, SUM(views) AS total_views
    FROM video_table
    GROUP BY channel_id, channel_name;
    """
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
button_clicked = st.button("Generate Output", key="generate_output_button_7")
if button_clicked:
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])

        st.write(df)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()
###################################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 8: What are the names of all the channels that have published videos in the year 2022?":
    """
    SELECT DISTINCT channel_name
    FROM video_table
    WHERE strftime('%Y', published_date) = '2022';
    """
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
button_clicked = st.button("Generate Output", key="generate_output_button_8")
if button_clicked:
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])

        st.write(df)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()
##############################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 9: What is the average duration of all videos in each channel, and what are their corresponding channel names?":
    """
    SELECT channel_name, AVG(duration) AS average_duration
    FROM video_table
    GROUP BY channel_name;
    """
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
button_clicked = st.button("Generate Output", key="generate_output_button_9")
if button_clicked:
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])

        st.write(df)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()
########################################################################################################################
import streamlit as st
import sqlite3
import pandas as pd

# Dictionary mapping questions to SQL queries
question_queries = {
    "Question 10: Which videos have the highest number of comments, and what are their corresponding channel names?":
    """
    SELECT v.video_id, v.title, v.channel_name, v.comments
    FROM video_table v
    JOIN (
        SELECT video_id, MAX(comments) AS max_comments
        FROM video_table
        GROUP BY video_id
    ) max_comments_table
    ON v.video_id = max_comments_table.video_id
    AND v.comments = max_comments_table.max_comments
    ORDER BY v.comments DESC;
    """
    # Add other questions and queries accordingly
}

# Set the default selected question
selected_question = list(question_queries.keys())[0]

# Streamlit UI

# Display selected question
st.header(selected_question)

# Execute SQL query and display output based on the selected question
button_clicked = st.button("Generate Output", key="generate_output_button_10")
if button_clicked:
    selected_query = question_queries.get(selected_question, "No query available")
    st.header("Query Output:")
    try:
        # SQLite Connection
        sqlite_connection = sqlite3.connect('your_database.db')
        with sqlite_connection:
            result = sqlite_connection.execute(selected_query)
            data = result.fetchall()
            df = pd.DataFrame(data, columns=[desc[0] for desc in result.description])

        st.write(df)
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
    finally:
        sqlite_connection.close()