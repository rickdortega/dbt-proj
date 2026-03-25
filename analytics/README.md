# 🛒 Olist E-Commerce Analytics (dbt Project)

Welcome to the data transformation layer for the Olist Brazilian E-Commerce dataset. This dbt project takes raw, messy transactional data from our Postgres `oltp` schema and transforms it into clean, reliable dimensional models for business reporting.

## 🏗️ Project Architecture

This project follows dbt best practices, splitting models into two distinct layers:

### 1. Staging (`models/staging/`)
The prep kitchen. These models pull directly from the raw `oltp` tables using the `{{ source() }}` macro. 
* **Purpose:** Light cleanup, standardizing column names (translating Portuguese to English), casting string timestamps into actual dates, and fixing typos.
* **Rule:** We NEVER join tables in the staging layer. One raw table = one staging model.

### 2. Marts (`models/marts/`)
The business logic. These models pull from the staging layer using the `{{ ref() }}` macro.
* **Purpose:** Heavy transformations, joins, and aggregations. 
* **Output:** This layer produces the final `dim_customers` and `fact_orders` tables that are exposed to our BI tools and executive dashboards.

## 🏃‍♂️ Helpful dbt Commands

To execute this project locally, make sure your Postgres Docker container is running, then use the following commands:

* `dbt debug` - Verifies your connection to the Postgres database.
* `dbt run` - Compiles the SQL and builds the views/tables in your data warehouse.
* `dbt test` - Runs data quality tests (e.g., checking for nulls or non-unique IDs).
* `dbt docs generate` & `dbt docs serve` - Compiles and launches this project's data dictionary website in your browser.

## 📝 Conventions
* All timestamps are cast to UTC.
* Monetary values are stored in Brazilian Real (BRL) but are cleanly aggregated in the `fact_orders` table.
* Product categories are translated to English via the `stg_product_category_name_translation` model.