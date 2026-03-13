import pandas as pd
from sqlalchemy import create_engine, text
import kaggle
import zipfile
import os
import glob
import time

# 1. Authenticate and Download the Dataset from Kaggle
zip_filename = 'brazilian-ecommerce.zip'
extract_folder = 'olist_data'

if not os.path.exists(extract_folder):
    print("Downloading Olist dataset from Kaggle...")
    kaggle.api.dataset_download_files('olistbr/brazilian-ecommerce', path='.', unzip=False)
    
    print("Extracting files...")
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
else:
    print("Data already downloaded and extracted. Skipping download.")

# 2. Connect to Docker Postgres (with a brief pause to let Postgres boot up)
print("Connecting to PostgreSQL...")
time.sleep(3) # Gives a fresh Docker container time to accept connections
engine = create_engine('postgresql://postgres:postgres@localhost:5433/warehouse')

# 3. Create the 'oltp' schema if it doesn't exist
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS oltp;"))
    conn.commit() # Required for SQLAlchemy 2.0+

# 4. Dynamically find all CSV files and load them
csv_files = glob.glob(f'{extract_folder}/*.csv')

print(f"Found {len(csv_files)} files. Starting ingestion...")

for file_path in csv_files:
    # Clean up the file name to create a neat table name
    # e.g., 'olist_customers_dataset.csv' -> 'customers'
    base_name = os.path.basename(file_path).replace('.csv', '')
    table_name = base_name.replace('olist_', '').replace('_dataset', '')
    
    print(f"Loading {table_name}...")
    
    # Read and load in chunks to manage memory
    chunksize = 20000
    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunksize)):
        if i == 0:
            # First chunk: replace the table if it exists
            chunk.to_sql(table_name, engine, schema='oltp', if_exists='replace', index=False)
        else:
            # Subsequent chunks: append the data
            chunk.to_sql(table_name, engine, schema='oltp', if_exists='append', index=False)

print("All real-world data successfully loaded into the oltp schema!")