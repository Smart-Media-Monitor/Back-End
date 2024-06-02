# Smart Media Monitor

This README provides instructions for setting up the project environment, including installing dependencies, setting up the database, and running the necessary scripts.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or later
- PostgreSQL

## Installation

### Step 1: Install Python Dependencies

First, clone the repository and navigate to the project directory. Then, install the required Python packages using pip:

pip install -r requirements.txt

### Step 2: Set Up PostgreSQL

Update your package lists and install PostgreSQL:

sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

### Step 3: Configure PostgreSQL

Switch to the PostgreSQL user and create a new database user and database:

sudo -i -u postgres
psql

In the PostgreSQL prompt, run the following commands:

CREATE USER hassan WITH PASSWORD 'mhp78692';
CREATE DATABASE smart_media_monitor;
GRANT ALL PRIVILEGES ON DATABASE smart_media_monitor TO hassan;
\q

Exit the PostgreSQL user session:

exit

### Step 4: Create Tables in the Database

Connect to the newly created database and create the required tables:

psql -h localhost -U hassan -d smart_media_monitor

In the PostgreSQL prompt, run the following commands to create the `users` and `comments` tables:

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    channel_id VARCHAR(50)
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Comment TEXT,
    Likes INTEGER,
    Time TIMESTAMP,
    Reply_Count INTEGER,
    Label VARCHAR(255),
    Label_Score FLOAT,
    Video_ID VARCHAR(255),
    Comment_Id INTEGER
);

\q

### Step 5: Populate the Database

Run the `comments_to_db.py` script to populate the `comments` table:

python comments_to_db.py

Connect to the database again to create the `summaries` table:

psql -h localhost -U hassan -d smart_media_monitor

In the PostgreSQL prompt, run the following command to create the `summaries` table:

CREATE TABLE summaries (
    id SERIAL PRIMARY KEY,
    Label VARCHAR(255),
    Summary TEXT
);

\q

Run the `summaries_to_db.py` script to populate the `summaries` table:

python summaries_to_db.py

### Step 6: Start the API

Finally, run the API:

python api.py

## Usage

The API should now be running and accessible. You can use it to interact with the `comments` and `summaries` data and the chatbots. Detailed API documentation can be added here to guide users on how to make requests and what endpoints are available.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
