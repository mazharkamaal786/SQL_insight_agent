# SQL Insight Agent (MCP)

Ask questions about a MySQL database in plain English and get answers backed by real SQL. This project is an MCP (Model Context Protocol) server that gives Claude safe, read-only access to a MySQL database.

## How it works

You (plain English) → Claude Desktop → MCP server (Python) → MySQL → results → Claude explains the insight

## Features

- `get_schema` tool: lets Claude discover tables and columns
- `run_sql_query` tool: runs a single SELECT query and returns the rows
- Two layers of safety:
  1. Python blocks anything that isn't a single SELECT (INSERT, UPDATE, DELETE, DROP, etc.)
  2. A dedicated MySQL user with SELECT-only privileges
- Automatic `LIMIT 100` on queries that have no limit

## Tech stack

Python, MySQL, PyMySQL, MCP (Python SDK), Jupyter Notebook, Claude Desktop

## Demo

![Claude answering a question](screenshot/claude_answer.png)
![Another question answered from MySQL](screenshot/claude_answer_2.png)

## Setup

1. Clone the repo and create a virtual environment:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
2. Create a MySQL database `insights_db` and load `sales.csv` using `01_load_data.ipynb`.
3. Create a read-only user:
   CREATE USER 'claude_reader'@'localhost' IDENTIFIED BY 'your_password';
   GRANT SELECT ON insights_db.* TO 'claude_reader'@'localhost';
4. Copy `.env.example` to `.env` and fill in your credentials.
5. Add the server to Claude Desktop's `claude_desktop_config.json`:
   {
     "mcpServers": {
       "sql-insight-agent": {
         "command": "path\\to\\venv\\Scripts\\python.exe",
         "args": ["path\\to\\server.py"]
       }
     }
   }
6. Fully quit and reopen Claude Desktop.

## Example questions

- Which region has the highest total sales?
- Who are the top 3 salespeople and what share of sales does each contribute?
- Which month had the highest sales compared to the monthly average?

## Dataset

`sales.csv` is a synthetic sales dataset (500 rows) generated for this demo.

## Author

Mazhar Kamaal
[LinkedIn](https://linkedin.com/in/mazhar-kamal-2599963a9) | [GitHub](https://github.com/mazharkamaal786) | mazharkamaal786@gmail.com
