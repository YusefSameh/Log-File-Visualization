import pymysql
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import argparse

def visualize(output_file):
    """
    Fetches log data from the database and generates visualizations.

    Args:
        output_file (str): The file path where the plot image will be saved.
    """
    # Establish a connection to the database
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        db='mydatabase',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            # Retrieve log data from the database
            sql = "SELECT `Date`, `Time`, `Level`, `Message`, `Random Number` FROM logs"
            cursor.execute(sql)
            rows = cursor.fetchall()

            # Convert the retrieved data into a pandas DataFrame
            log_df = pd.DataFrame(rows, columns=['Date', 'Time', 'Level', 'Message', 'Random Number'])

            # Clean the DataFrame by removing any accidental header rows
            log_df = log_df[log_df['Date'] != 'Date']

            # Group log data by Time, Level, and Random Number, then count occurrences
            grouped_logs = log_df.groupby(['Time', 'Level', 'Random Number']).size().reset_index(name='Count')

            # Define a color map for different log levels
            color_map = {
                'INFO': 'blue',
                'WARNING': 'orange',
                'ERROR': 'red',
                'DEBUG': 'green',
                'CRITICAL': 'purple'
            }

            # Count occurrences of each log level
            log_level_counts = log_df['Level'].value_counts().to_dict()

            # Create a bar chart for the distribution of log levels
            bar_chart = go.Bar(
                x=list(log_level_counts.keys()),
                y=list(log_level_counts.values()),
                name='Log Levels',
                marker=dict(color=[color_map[level] for level in log_level_counts.keys()])
            )
        
            # Create subplots: one for the bar chart and another for log levels over time
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Distribution of Log Levels', 'Log Levels Over Time'),
                shared_xaxes=True
            )
        
            # Add the bar chart to the first subplot
            fig.add_trace(bar_chart, row=1, col=1)
        
            # Plot lines for each log level over time in the second subplot
            for level in grouped_logs['Level'].unique():
                level_data = grouped_logs[grouped_logs['Level'] == level]
                fig.add_trace(
                    go.Scatter(
                        x=level_data['Time'],
                        y=level_data['Random Number'],
                        mode='lines',
                        name=level,
                        line=dict(color=color_map[level])
                    ),
                    row=2, col=1
                )
        
            # Update axis titles for better readability
            fig.update_xaxes(title_text="Log Level", row=1, col=1)
            fig.update_yaxes(title_text="Count", row=1, col=1)
            fig.update_xaxes(title_text="Time", row=2, col=1)
            fig.update_yaxes(title_text="Random Number", row=2, col=1)
        
            # Adjust the layout for a more polished presentation
            fig.update_layout(
                height=800,
                title_text="Combined Log Visualizations"
            )

            # Save the final plot as an image file
            fig.write_image(output_file)

    finally:
        # Ensure the database connection is closed
        conn.close()

if __name__ == "__main__":
    # Parse command-line arguments for the output file path
    parser = argparse.ArgumentParser(description="Visualize log data from the database.")
    parser.add_argument(
        'output_file',
        type=str,
        help="The file path where the plot image will be saved. Example: output.png"
    )

    # Call the visualize function with the provided output file path
    args = parser.parse_args()
    visualize(args.output_file)
