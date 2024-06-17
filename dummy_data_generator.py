import hashlib
import csv
from faker import Faker

# Initialize the Faker library
fake = Faker()

# Function to generate a SHA-256 hash of a given string
def generate_hash(input_string):
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

# Function to create a CSV file with dummy hashes
def generate_dummy_data(file_path, num_records):
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header
        csvwriter.writerow(['hash'])
        
        for _ in range(num_records):
            # Generate a fake file name
            fake_file_name = fake.file_name()
            # Generate hash for the fake file name
            file_hash = generate_hash(fake_file_name)
            # Write the hash to the CSV file
            csvwriter.writerow([file_hash])

# Generate dummy data and write to a CSV file
dummy_data_file_path = 'dummy_nsrl_data.csv'  # Path to the output CSV file
num_dummy_records = 10000000  # Number of dummy records to generate

generate_dummy_data(dummy_data_file_path, num_dummy_records)
print(f"Generated {num_dummy_records} dummy records in {dummy_data_file_path}.")
