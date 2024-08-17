# Log File Visualization

This Python script reads log files, processes the data, and generates visualizations using Plotly. The visualizations include a bar chart showing the distribution of log levels and a time-series line plot displaying log levels and additional info over time.

## Features

- Parses log files into structured format for analysis.
- Displays log level distribution with a bar chart.
- Visualizes log levels over time with a line plot.
- Flexible and easy to extend.

## Requirements

- Python 3.x
- `pandas`
- `plotly`

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
2- **Run the script**
   To run the script, pass the path to your log file as an argument:
   ```bash
   python log_visualization.py <log_file>
   ```
   Example:
   ```bash
   python log_visualization.py /path/to/log/file.log
   ```

## Functions 

- **parse_log_file(log_file)**: Reads and parses the log file, breaking each log entry into its components (Date, Time, Level, Message, Additional Info).
- **main(log_file)**: Main function that calls the parse_log_file function, processes the logs, and generates visualizations.

## Visualization

- **Distribution of Log Levels**: A bar chart showing the counts of different log levels (INFO, WARNING, ERROR, etc.).
- **Log Levels Over Time**: A time-series line plot showing how log levels and additional info change over time.

## Customization

- You can change the color of the log levels in the chart by modifying the color_map dictionary in the script.

## Notes

- The script reads the log file once and generates static visualizations. To analyze real-time data, rerun the script as new logs are generated.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
