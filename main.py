# STEP 1A
# Import SQL Library and Pandas
import sqlite3
from pathlib import Path

import pandas as pd

# STEP 1B
# Connect to the database
conn = sqlite3.connect(Path(__file__).resolve().with_name("data.sqlite"))


# STEP 2
# Select employee numbers and last names for all employees.
df_first_five = pd.read_sql("SELECT employeeNumber, lastName FROM employees", conn)

# STEP 3
df_five_reverse = pd.read_sql("SELECT lastName, employeeNumber FROM employees", conn)

# STEP 4
df_alias = pd.read_sql("SELECT lastName, employeeNumber AS ID FROM employees", conn)

# STEP 5
df_executive = pd.read_sql(
    """
    SELECT *,
           CASE
               WHEN jobTitle IN ('President', 'VP Sales', 'VP Marketing')
                   THEN 'Executive'
               ELSE 'Not Executive'
           END AS role
    FROM employees
    """,
    conn,
)

# STEP 6
df_name_length = pd.read_sql(
    "SELECT LENGTH(lastName) AS name_length FROM employees", conn
)

# STEP 7
df_short_title = pd.read_sql(
    "SELECT SUBSTR(jobTitle, 1, 2) AS short_title FROM employees", conn
)

# STEP 8
sum_total_price = pd.read_sql(
    "SELECT SUM(ROUND(priceEach * quantityOrdered)) AS total_price FROM orderDetails",
    conn,
)["total_price"]

# STEP 9
df_day_month_year = pd.read_sql(
    """
    SELECT orderDate,
           STRFTIME('%d', orderDate) AS day,
           STRFTIME('%m', orderDate) AS month,
           STRFTIME('%Y', orderDate) AS year
    FROM orders
    """,
    conn,
)

conn.close()


if __name__ == "__main__":
    print("SQL SELECT Lab Results")
    for title, result in (
        ("Step 2: Employee numbers and last names", df_first_five),
        ("Step 3: Last names and employee numbers", df_five_reverse),
        ("Step 4: Employee numbers aliased as ID", df_alias),
        ("Step 5: Executive roles", df_executive),
        ("Step 6: Last name lengths", df_name_length),
        ("Step 7: Short job titles", df_short_title),
    ):
        print(f"\n{title}")
        print(result.to_string(index=False))

    print("\nStep 8: Total of rounded order line prices")
    print(f"{sum_total_price.iloc[0]:,.0f}")

    print("\nStep 9: Order dates (first 10 rows)")
    print(df_day_month_year.head(10).to_string(index=False))
    print(f"Total orders: {len(df_day_month_year)}")
