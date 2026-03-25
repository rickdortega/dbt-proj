# Rescuing Your Data Pipeline: A dbt & ELT project

Welcome to the companion repository for the Medium article series: Rescuing Your Data Pipeline from Spaghettification.

This project demonstrates the transition from fragile, legacy ETL pipelines to modern, robust ELT (Extract, Load, Transform) architecture using Python, PostgreSQL, and dbt (data build tool).

Instead of using perfectly clean foo/bar dummy data, this project uses the real-world Olist Brazilian E-Commerce Dataset (100,000+ real orders) to show how dbt handles messy, untyped data, standardizes it in a staging layer, and builds production-ready dimensional models.

## The Article Series
- Part 1: [Link to Part 1] - The What & Why: Rescuing Your Warehouse from Spaghettification
- Part 2: [Link to Part 2] - The When & How: Stop Writing DDL and Start Writing dbt
(Parts 3 and 4 coming soon!)

## The Tech Stack
- Extraction & Loading (EL): Python (Pandas, SQLAlchemy, Kaggle API)
- Data Warehouse: PostgreSQL (Hosted locally via Docker)
- Transformation (T): dbt Core

## Getting Started
Follow these instructions to get the entire data stack running on your local machine.

### Prerequisites
Before you begin, ensure you have the following installed:

1. Docker & Docker Compose (To run the local PostgreSQL data warehouse)
2. Python 3.9+ (To run the extraction script and dbt)
3. A Kaggle Account (To download the real-world dataset)

__Step 1: Clone the Repository__
```bash
git clone https://github.com/rickdortega/dbt-proj.git
cd dbt-proj
```

__Step 2: Set Up Your Python Environment__

It is highly recommended to use a virtual environment to keep your dependencies clean.
```bash
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

__Step 3: Configure Your Kaggle API Key__

The load_data.py script automatically downloads the Olist dataset from Kaggle. To allow this, you need a Kaggle API token.

1. Log in to Kaggle.
2. Go to your Account Settings and click "Create New API Token". This will download a `kaggle.json` file.
3. Place this file in the correct hidden directory on your machine:
    - macOS/Linux: `~/.kaggle/kaggle.json`
    - Windows: `C:\Users\<Your-Username>\.kaggle\kaggle.json`
4. macOS/Linux only: Secure the file by running `chmod 600 ~/.kaggle/kaggle.json`.


__Step 4: Spin Up the Data Warehouse__

We use Docker to spin up a fresh, empty PostgreSQL database that will act as our target data warehouse.
```bash
# Start the container in detached mode (-d)
docker-compose up -d
```
_Note: The database runs on port 5433 with the username postgres and password postgres._

__Step 5: Extract and Load the Raw Data (EL)__

Run the Python ingestion script. This will download the Kaggle dataset, create a raw `oltp` schema in Postgres, and dump the raw CSV data into the database.
```bash
python load_data.py
```

__Step 6: Configure dbt__
dbt needs to know how to connect to your local Postgres database. This is configured in a `profiles.yml` file.
Create a hidden `.dbt` folder in your home directory and add the `profiles.yml` file.
- macOS/Linux: `~/.dbt/profiles.yml`
- Windows: `C:\Users\<Your-Username>\.dbt\profiles.yml`

Paste the following connection details into that file:
```yaml
analytics:
  outputs:
    dev:
      type: postgres
      threads: 1
      host: localhost
      port: 5433
      user: postgres
      pass: postgres
      dbname: warehouse
      schema: dbt_dev
  target: dev
```

__Step 7: Transform the Data (T)__
Navigate into the dbt project folder and test your database connection:
```bash
cd analytics
dbt debug
```
If all checks pass (green text), you are ready to build the pipeline! Run the following command to execute the DAG, clean the staging data, and build the final business-ready models:
```bash
dbt run
```
## Project Structure
- `docker-compose.yml`: Infrastructure configuration for the local Postgres warehouse.
- `load_data.py`: The Python ELT script that ingests the raw Kaggle data.
- `analytics/`: The core dbt project folder.
- `models/staging/`: Where raw data is cleaned, cast, and standardized.
- `models/marts/`: Where business logic, aggregations, and joins happen (the final reporting tables).
- `dbt_project.yml`: The main configuration file for the dbt project.