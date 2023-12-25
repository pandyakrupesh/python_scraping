import pymysql

# Add your SQL credentials here
host = 'localhost'
db_user = 'krupesh'
db_password = 'krupesH3009'
port = 3306
database = 'linkedin'
table_name = 'linkedin_jobs_details'


def create_database():
    """
    Function to create the database if it doesn't exist.
    """
    con = pymysql.connect(host=host, port=port, user=db_user, passwd=db_password)
    cur = con.cursor()
    cur.execute(f'CREATE DATABASE IF NOT EXISTS {database}')
    cur.close()
    con.close()


def connection():
    """
    Function to establish a connection to the database.
    """
    con = pymysql.connect(host=host, port=port, user=db_user, passwd=db_password, database=database)
    return con


def create_table():
    """
    Function to create a table in the database if it doesn't exist.
    """
    con = connection()
    cur = con.cursor()

    try:
        # Add your table query here
        table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (Job_Post_URL VARCHAR(255), Job_Post_Title VARCHAR(255), Company_Linkedin_URL VARCHAR(255), Industry VARCHAR(255), Company_Name VARCHAR(255), Job_Post_Text LONGTEXT, Company_Headquarters VARCHAR(255), Company_Number_of_Employees VARCHAR(255), UNIQUE KEY `Job_Post_URL` (`Job_Post_URL`));"
        cur.execute(table_query)
    except Exception as e:
        print(e)
        pass

    con.commit()
    con.close()


def insert_into_table(item, table_name):
    """
    Function to insert data into the table.
    Arguments:
        - item: Dictionary containing the data to be inserted.
        - table_name: Name of the table to insert data into.
    """
    con = connection()
    cur = con.cursor()

    field_list = []
    value_list = []
    for field in item:
        field_list.append(str(field).strip())
        value_list.append(str(item[field]).replace("'", "’").strip())

    fields = ','.join(field_list)
    values = "','".join(value_list)
    insert_db = f"INSERT IGNORE INTO {table_name} " + "(" + fields + ") VALUES ('" + values + "')"

    try:
        cur.execute(insert_db)
        con.commit()
        print('Data Inserted')
    except Exception as e:
        print(e)
        pass

    cur.close()
    con.close()


def select_from_table(table_name, columns='*', condition=''):
    """
    Function to select data from the table.
    Arguments:
        - table_name: Name of the table to select data from.
        - columns: Columns to select (string or list), defaults to '*' (all columns).
        - condition: Condition to apply while selecting data, defaults to empty string.
    Returns:
        - List of selected rows from the table.
    """
    con = connection()
    cur = con.cursor()

    try:
        select_query = f"SELECT {columns} FROM {table_name}"
        if condition:
            select_query += f" WHERE {condition}"
        cur.execute(select_query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(e)
        pass

    cur.close()
    con.close()


def update_table(table_name, set_values, condition=''):
    """
    Function to update data in the table.
    Arguments:
        - table_name: Name of the table to update.
        - set_values: Values to set in the update statement.
        - condition: Condition to apply while updating data, defaults to empty string.
    """
    con = connection()
    cur = con.cursor()

    try:
        update_query = f"UPDATE {table_name} SET {set_values}"
        if condition:
            update_query += f" WHERE {condition}"
        cur.execute(update_query)
        con.commit()
        print('Table updated')
    except Exception as e:
        print(e)
        pass

    cur.close()
    con.close()


def delete_from_table(table_name, condition=''):
    """
    Function to delete data from the table.
    Arguments:
        - table_name: Name of the table to delete data from.
        - condition: Condition to apply while deleting data, defaults to empty string.
    """
    con = connection()
    cur = con.cursor()

    try:
        delete_query = f"DELETE FROM {table_name}"
        if condition:
            delete_query += f" WHERE {condition}"
        cur.execute(delete_query)
        con.commit()
        print('Rows deleted')
    except Exception as e:
        print(e)
        pass

    cur.close()
    con.close()


def execute_query(query):
    """
    Function to execute custom SQL queries.
    Arguments:
        - query: SQL query to execute.
    """
    con = connection()
    cur = con.cursor()

    try:
        cur.execute(query)
        con.commit()
        print('Query executed successfully')
    except Exception as e:
        print(e)
        pass

    cur.close()
    con.close()


def fetch_table_columns(table_name):
    """
    Function to fetch column names of the table.
    Arguments:
        - table_name: Name of the table to fetch column names from.
    Returns:
        - List of column names of the table.
    """
    con = connection()
    cur = con.cursor()

    try:
        cur.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [column[0] for column in cur.fetchall()]
        return columns
    except Exception as e:
        print(e)
        pass

    cur.close()
    con.close()


def drop_table(table_name):
    """
    Function to drop the table from the database.
    Arguments:
        - table_name: Name of the table to drop.
    """
    con = connection()
    cur = con.cursor()

    try:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        con.commit()
        print('Table dropped')
    except Exception as e:
        print(e)
        pass

    cur.close()
    con.close()


def count_rows(table_name):
    """
    Function to count the number of rows in the table.
    Arguments:
        - table_name: Name of the table to count rows.
    Returns:
        - Number of rows in the table.
    """
    con = connection()
    cur = con.cursor()

    try:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cur.fetchone()[0]
        return count
    except Exception as e:
        print(e)
        pass

    cur.close()
    con.close()


def check_table_exists(table_name):
    """
    Function to check if a table exists in the database.
    Arguments:
        - table_name: Name of the table to check.
    Returns:
        - Boolean indicating whether the table exists or not.
    """
    con = connection()
    cur = con.cursor()

    try:
        cur.execute("SHOW TABLES")
        tables = [table[0] for table in cur.fetchall()]
        if table_name in tables:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        pass

    cur.close()
    con.close()
