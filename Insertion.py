import pymysql
import sys
from log_visualization import parse_log_file

# Establish a connection to the MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='mydatabase',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def main(log_file):
    """
    Parses the log file and inserts the records into the database.

    Args:
        log_file (str): Path to the log file to be parsed and inserted into the database.
    """
    try:
        with conn.cursor() as cursor:
            # SQL query to insert parsed log data into the 'logs' table
            sql = """
                INSERT INTO `logs` 
                (`Date`, `Time`, `Level`, `Message`, `Random Number`) 
                VALUES (%s, %s, %s, %s, %s)
            """
            
            # Parse the log file to extract necessary information
            parsed_logs = parse_log_file(log_file)
            
            # Execute the SQL query with the parsed log data
            cursor.executemany(sql, parsed_logs)
            
            # Commit the transaction to save the changes in the database
            conn.commit()

        print("Record inserted successfully")
    
    finally:
        # Ensure the database connection is closed
        conn.close()

if __name__ == "__main__":
    """
    Entry point of the script. Ensures correct command-line arguments are provided,
    then calls the main function with the log file path.
    """
    if len(sys.argv) != 2:
        print("Usage: python Insertion.py <log_file>")
    else:
        log_file = sys.argv[1]
        main(log_file)
