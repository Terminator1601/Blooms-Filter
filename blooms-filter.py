from bloom_filter2 import BloomFilter
import csv

# Initialize Bloom filter with an estimated capacity and false positive rate
bloom_filter = BloomFilter(max_elements=1000000, error_rate=0.001)

# Function to load NSRL database hashes from CSV into the Bloom filter
def load_nsrl_into_bloom_filter(file_path):
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            file_hash = row[0].strip().lower()
            bloom_filter.add(file_hash)

# Function to check if a hash is in the Bloom filter
def check_hash_in_bloom_filter(file_hash):
    hashed_value = file_hash.strip().lower()
    return hashed_value in bloom_filter

# Main function to load data into Bloom filter and check hashes
def main():
    # Load dummy data into Bloom filter
    dummy_data_file_path = 'dummy_nsrl_data.csv'  # Path to the generated CSV file
    load_nsrl_into_bloom_filter(dummy_data_file_path)
    
    # Check if a specific hash is in the Bloom filter
    test_hash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'  # Example SHA-256 hash
    if check_hash_in_bloom_filter(test_hash):
        print("Hash is in the NSRL database.")
    else:
        print("Hash is NOT in the NSRL database.")

if __name__ == "__main__":
    main()
