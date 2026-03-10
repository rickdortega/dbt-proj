from faker import Faker
import psycopg2
import random

fake = Faker()

# Connect using the exposed port (5433)
conn = psycopg2.connect(
    "host=localhost port=5433 dbname=warehouse user=postgres password=postgres"
)
cur = conn.cursor()

# 1. Populate Customers
print("Populating customers...")
for _ in range(100):
    cur.execute(
        "INSERT INTO oltp.customers (email, first_name, last_name, created_at) VALUES (%s, %s, %s, %s)",
        (fake.email(), fake.first_name(), fake.last_name(), fake.date_time_this_year()),
    )

# 2. Populate Products
print("Populating products...")
product_types = ["Electronics", "Clothing", "Home", "Books", "Software"]
for _ in range(20):
    cur.execute(
        "INSERT INTO oltp.products (product_type, name, price) VALUES (%s, %s, %s)",
        (
            random.choice(product_types),
            fake.word().capitalize(),
            round(random.uniform(10.0, 500.0), 2),
        ),
    )

# --- Fetch the generated IDs to use as Foreign Keys ---
cur.execute("SELECT customer_id FROM oltp.customers")
customer_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT product_id FROM oltp.products")
product_ids = [row[0] for row in cur.fetchall()]

# 3. Populate Orders
print("Populating orders...")
for _ in range(150):
    cur.execute(
        "INSERT INTO oltp.orders (customer_id, order_date) VALUES (%s, %s)",
        (random.choice(customer_ids), fake.date_time_this_month()),
    )

# Fetch generated Order IDs
cur.execute("SELECT order_id FROM oltp.orders")
order_ids = [row[0] for row in cur.fetchall()]

# 4. Populate Order Items
print("Populating order items...")
for order_id in order_ids:
    # Give each order between 1 and 4 random items
    for _ in range(random.randint(1, 4)):
        cur.execute(
            "INSERT INTO oltp.order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
            (order_id, random.choice(product_ids), random.randint(1, 5)),
        )

# Commit the transaction and close
conn.commit()
cur.close()
conn.close()

print("Database populated successfully!")
