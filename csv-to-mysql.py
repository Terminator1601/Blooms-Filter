import hashlib
import csv
from faker import Faker
import mysql.connector

# Initialize the Faker library
fake = Faker()

# Function to generate a SHA-256 hash of a given string
def generate_hash(input_string):
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

# Function to connect to MySQL and create a table for dummy data
def create_mysql_table(num_columns):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="rishi",
            password="admin",
            database="NSRL Dummy Database"
        )
        cursor = conn.cursor()

        # Drop table if it exists (optional, uncomment if needed)
        # cursor.execute("DROP TABLE IF EXISTS dummy_data")

        # Create table
        create_table_query = f"CREATE TABLE IF NOT EXISTS dummy_data (id INT AUTO_INCREMENT PRIMARY KEY, "
        for i in range(1, num_columns + 1):
            create_table_query += f"hash{i} VARCHAR(255)"
            if i != num_columns:
                create_table_query += ", "
        create_table_query += ")"
        cursor.execute(create_table_query)

        conn.commit()
        print("MySQL table 'dummy_data' created successfully.")

        return conn, cursor

    except mysql.connector.Error as error:
        print(f"Error while connecting to MySQL: {error}")
        return None, None

# Function to insert dummy data into MySQL table
def insert_dummy_data(conn, cursor, num_records, num_columns):
    try:
        insert_query = f"INSERT INTO dummy_data ("
        for i in range(1, num_columns + 1):
            insert_query += f"hash{i}"
            if i != num_columns:
                insert_query += ", "
        insert_query += ") VALUES ("
        insert_query += ", ".join(["%s"] * num_columns)
        insert_query += ")"

        with open('dummy_nsrl_data.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row
            batch_size = 1000
            records = []
            for row in csvreader:
                records.append(tuple(row))
                if len(records) == batch_size:
                    cursor.executemany(insert_query, records)
                    conn.commit()
                    records = []

            # Insert remaining records
            if records:
                cursor.executemany(insert_query, records)
                conn.commit()

        print(f"Inserted {num_records} records into MySQL table 'dummy_data'.")

    except mysql.connector.Error as error:
        print(f"Error inserting data into MySQL table: {error}")

# Main function to generate dummy data and store in MySQL
def main():
    num_dummy_records = 10000000  # Number of dummy records to generate
    num_columns = 3  # Number of columns in the MySQL table

    # Connect to MySQL and create table
    conn, cursor = create_mysql_table(num_columns)
    if conn and cursor:
        # Generate dummy data and insert into MySQL table
        insert_dummy_data(conn, cursor, num_dummy_records, num_columns)

        # Close connection
        cursor.close()
        conn.close()
        print("MySQL connection closed.")

if __name__ == "__main__":
    main()
