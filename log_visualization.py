import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys

def parse_log_file(log_file):
    """
    Reads and parses the log file into a structured format.

    Args:
        log_file (str): Path to the log file.

    Returns:
        list: A list of parsed log entries, where each entry is a list of [Date, Time, Level, Message, Additional Info].
    """
    with open(log_file, 'r') as f:
        log_lines = f.readlines()
    
    parsed_logs = []
    for line in log_lines:
        elements = line.strip().split(" - ")

        # Split message from Random Number
        message_parts = elements[2].strip().split(". ")
        elements = elements[:2] + [message_parts[0], message_parts[1]] + elements[3:]
        # Split Date and Time
        time_parts = elements[0].strip().split(" ")
        elements = [time_parts[0], time_parts[1]] + elements[1:]
        # Convert Random Number to Integer
        additional_info = int(elements[4].strip("(").strip(")"))
        elements = elements[:4] + [additional_info]
        # Collect the processed log data
        parsed_logs.append(elements)
    
    return parsed_logs

def main(log_file):
    """
    Main function to process log file and visualize data.

    Args:
        log_file (str): Path to the log file.
    """
    # Load and parse logs
    parsed_logs = parse_log_file(log_file)

    # Extract log levels for plotting
    log_levels = [log[2] for log in parsed_logs]

    # Create a DataFrame from the parsed logs
    log_df = pd.DataFrame(parsed_logs, columns=['Date', 'Time', 'Level', 'Message', 'Additional Info'])

    # Convert Date and Time to datetime objects for time-series analysis
    log_df['DateTime'] = pd.to_datetime(log_df['Date'] + ' ' + log_df['Time'])

    # Group by datetime, level, and additional info, and count occurrences
    grouped_logs = log_df.groupby(['DateTime', 'Level', 'Additional Info']).size().reset_index(name='Count')

    # Define a color map for the log levels
    color_map = {
        'INFO': 'blue',
        'WARNING': 'orange',
        'ERROR': 'red',
        'DEBUG': 'green',
        'CRITICAL': 'purple'
    }

    # Count occurrences of each log level
    log_level_counts = {level: log_levels.count(level) for level in set(log_levels)}

    # Visualization 1: Bar chart showing the distribution of log levels
    bar_chart = go.Bar(
        x=list(log_level_counts.keys()),  # Use unique log levels for x-axis
        y=list(log_level_counts.values()),  # Use counts of each log level for y-axis
        name='Log Levels',
        marker=dict(color=[color_map[level] for level in log_level_counts.keys()])  # Apply color mapping for log levels
    )

    # Create a subplot with 2 rows
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Distribution of Log Levels', 'Log Levels Over Time'),
        shared_xaxes=True  # Option to share the x-axis between plots
    )

    # Add bar chart to the first row
    fig.add_trace(bar_chart, row=1, col=1)

    # Add a separate line for each log level in the second plot
    for level in grouped_logs['Level'].unique():
        level_data = grouped_logs[grouped_logs['Level'] == level]
        fig.add_trace(
            go.Scatter(
                x=level_data['DateTime'],
                y=level_data['Additional Info'],
                mode='lines',
                name=f'{level}',
                line=dict(color=color_map[level])  # Line color based on log level
            ),
            row=2, col=1
        )

    # Update x- and y-axis titles for both subplots
    fig.update_xaxes(title_text="Log Level", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=1)

    fig.update_xaxes(title_text="DateTime", row=2, col=1)
    fig.update_yaxes(title_text="Additional Info", row=2, col=1)

    # Adjust layout for better presentation
    fig.update_layout(
        height=800,  # Adjust the height of the overall plot
        title_text="Combined Log Visualizations"
    )

    # Show the combined plot
    fig.show()

if __name__ == "__main__":
    """
    Entry point for the script. Continuously updates visualization of the log file every 2 seconds.
    """
    log_file = sys.argv[1]
    main(log_file)
