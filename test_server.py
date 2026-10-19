from server import get_schema, run_sql_query

print(get_schema())
print()
print(run_sql_query("SELECT region, SUM(amount) AS total FROM sales GROUP BY region ORDER BY total DESC"))
print()
print(run_sql_query("DROP TABLE sales"))