# Log File Local Visualization and Database Insertion & Visualization

This repository contains Python scripts for parsing log files, visualizing the data, inserting parsed data into a MySQL database, and generating visualizations directly from the database. The visualizations are generated using Plotly, and the log data is stored in a MySQL database for further analysis.

## Features

- **Log Parsing**: Parses log files into a structured format for analysis.
- **Visualization**: Displays log level distribution with a bar chart and visualizes log levels over time with a line plot.
- **Database Insertion**: Inserts parsed log data into a MySQL database.
- **Database Visualization**: Fetches log data from the database and generates visualizations.

## Requirements

- Python 3.x
- MySQL Server
- The following Python packages are required:
   - `pandas`
   - `plotly`
   - `pymysql`
   - `argparse`
   - `kaleido`

You can install them using the following command:
```bash
pip install pandas plotly pymysql argparse kaleido
```
## Usage

1- **Prepare your log file**

   The log file must follow this format:
   ```php
   <date> <time> - <log level> - <message>. <additional info>
   ```
   Example log entries:
   ```yaml
   2024-08-16 10:00:01 - INFO - Data processed successfully. (234)
   2024-08-16 10:01:23 - WARNING - Disk space running low. (56)
   ```
2- **Run the visualization script**

   To run the script, pass the path to your log file as an argument:
   ```bash
   python log_visualization.py <log_file>
   ```
   Example:
   ```bash
   python log_visualization.py /path/to/log/file.log
   ```
3- **Run the database insertion script**
   
   To insert the parsed log data into a MySQL database:
   1. Ensure your MySQL server is running and the database is properly configured.
   2. Modify the database connection details in the script if necessary.
   3. Run the script with the path to your log file as an argument:
   ```bash
   python Insertion.py <log_file>
   ```
   Example:
   ```bash
   python Insertion.py /path/to/log/file.log
   ```
4- **Visualize data directly from the database**

   To generate visualizations from the data stored in the MySQL database:
   1. Ensure your MySQL server is running and the logs table contains data.
   2. Modify the database connection details in the script if necessary.
   3. Run the script with the path to the output file as an argument:
   ```bash
   python visualize_from_db.py <output_file>
   ```
   Example:
   ```bash
   python visualize_from_db.py output.png
   ```
## Functions 

- **`parse_log_file(log_file)`**: Reads and parses the log file, breaking each log entry into its components (Date, Time, Level, Message, Additional Info).
- **`main(log_file)` (in `log_visualization.py`)**: Main function that calls the parse_log_file function, processes the logs, and generates visualizations.
- **`main(log_file)` (in `Insertion.py`)**: Parses the log file and inserts the parsed records into a MySQL database.
- **`visualize(output_file)` (in `Visualization.py`)**: Fetches log data from the database and generates visualizations.

## Output

- **Visualization**:

   - **Distribution of Log Levels**: A bar chart showing the counts of different log levels (INFO, WARNING, ERROR, etc.).
   - **Log Levels Over Time**: A time-series line plot showing how log levels and additional info change over time.

- **Database**: Parsed log data is inserted into the specified MySQL database table.
- **Visualization from Database**: Generates and saves visualizations directly from the data stored in the database.

## Customization

- **Visualization**: You can change the color of the log levels in the chart by modifying the color_map dictionary in the scripts.
- **Database Connection**: Modify the connection parameters in the scripts to match your MySQL server configuration.

## Notes

- The script reads the log file once and generates static visualizations. To analyze real-time data, rerun the script as new logs are generated.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
