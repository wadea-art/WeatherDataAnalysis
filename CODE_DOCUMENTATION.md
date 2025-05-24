# Weather Data Analysis: Detailed Code Documentation

## Table of Contents
1. [Project Structure](#project-structure)
2. [Core Application File: weather_app.py](#core-application-file-weather_apppy)
3. [Data Processing](#data-processing)
4. [Visualization System](#visualization-system)
5. [Analytics Components](#analytics-components)
6. [Reporting System](#reporting-system)
7. [Helper Scripts](#helper-scripts)
8. [Configuration Files](#configuration-files)
9. [Best Practices and Code Patterns](#best-practices-and-code-patterns)
10. [Performance Considerations](#performance-considerations)

## Project Structure

The Weather Data Analysis project follows a modular architecture with distinct components handling different aspects of the application:

```
.
├── attached_assets/      # Data directory
│   └── weatherHistory.csv  # Main weather dataset
├── app.py                # Original Streamlit application (not in use)
├── weather_app.py        # Main Streamlit application
├── data_processing.py    # Data loading and cleaning functions
├── visualization.py      # Visualization components
├── analytics.py          # Statistical analysis functions
├── reporting.py          # Report generation
├── project_documentation.py  # Documentation generator
├── run.py                # Python runner script
├── run_weather_analysis.sh   # Bash runner script
├── DOCUMENTATION.md      # User documentation
└── CODE_DOCUMENTATION.md # Technical code documentation
```

This structure ensures separation of concerns and makes the codebase more maintainable by isolating specific functionalities into their own modules.

## Core Application File: weather_app.py

The `weather_app.py` file serves as the main entry point and integrates all components of the application. This Streamlit-based application orchestrates the data flow and user interface.

### Key Code Sections

#### Application Initialization
```python
# Set page configuration
st.set_page_config(
    page_title="Weather Data Analysis",
    page_icon="🌤️",
    layout="wide"
)

# Main title
st.title("🌤️ Weather Data Analysis")
st.subheader("Insights from Historical Weather Data")
```
This section configures the application's appearance and creates the main header elements. The `layout="wide"` parameter maximizes screen real estate for data visualizations.

#### Data Loading Function
```python
@st.cache_data
def load_data():
    # Load the data
    file_path = "attached_assets/weatherHistory.csv"
    df = pd.read_csv(file_path)
    
    # Basic data cleaning
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['Formatted Date'], utc=True)
    
    # Extract date components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    
    # Rename columns for easier access
    renamed_cols = {
        'Temperature (C)': 'temperature',
        'Apparent Temperature (C)': 'apparent_temp',
        'Humidity': 'humidity',
        'Wind Speed (km/h)': 'wind_speed',
        'Wind Bearing (degrees)': 'wind_bearing',
        'Visibility (km)': 'visibility',
        'Pressure (millibars)': 'pressure',
        'Precip Type': 'precip_type',
        'Summary': 'summary'
    }
    
    # Apply the renaming
    df = df.rename(columns=renamed_cols)
    
    return df
```
This function handles data loading with Streamlit's caching mechanism to improve performance. The `@st_cache_data` decorator ensures the function runs only once and caches the results, avoiding redundant data loading operations when the app reruns.

#### Tab-Based Interface
```python
# Data Analysis Sections
st.header("2. Basic Statistics")

# [... statistics calculation code ...]

# 3. Univariate Analysis
st.header("3. Univariate Analysis")

# [... univariate analysis code ...]

# 4. Time Series Analysis
st.header("4. Time Series Trends")

# [... time series code ...]

# 5. Bivariate Analysis
st.header("5. Bivariate Analysis")

# [... bivariate analysis code ...]

# 6. Key Questions
st.header("6. Key Questions to Explore")

# [... key questions code ...]

# 7. Summary Report
st.header("8. Summary of Findings")

# [... report generation code ...]
```
The application follows a sequential layout with distinct sections for different types of analysis. Each section is clearly demarcated with headers and contains specific visualizations and interactive elements.

#### PDF Report Generation
```python
# Function to convert markdown to PDF
def create_pdf_from_report(report_text):
    import io
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.units import inch
    
    # Create an in-memory buffer
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    # Create custom styles - use a different name to avoid conflicts
    title_style = ParagraphStyle(name='DocTitle', 
                             parent=styles['Heading1'], 
                             fontSize=16, 
                             alignment=TA_CENTER)
    
    # Process the markdown text into reportlab elements
    elements = []
    
    # [... markdown parsing code ...]
    
    # Build the PDF
    doc.build(elements)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

# Create a download button for the PDF report
st.download_button(
    label="📥 Download Report as PDF",
    data=create_pdf_from_report(report_content),
    file_name="weather_data_analysis_report.pdf",
    mime="application/pdf",
)
```
This code section implements PDF report generation using the ReportLab library. The function parses markdown text into appropriate ReportLab elements and assembles a formatted PDF document. The function is called when the user clicks the download button.

## Data Processing

The data processing functionality is implemented in `data_processing.py` with two main functions:

### Load Data Function
```python
def load_data(file_path):
    """
    Load the weather data from CSV file
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
        
    Returns:
    --------
    pandas.DataFrame
        Loaded weather data
    """
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {e}")
```
This function provides error handling during the data loading process and returns a Pandas DataFrame.

### Clean Data Function
```python
def clean_data(df):
    """
    Clean and preprocess the weather data
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Raw weather data
        
    Returns:
    --------
    pandas.DataFrame
        Cleaned and preprocessed weather data
    """
    # Make a copy to avoid modifying the original dataframe
    df_cleaned = df.copy()
    
    # Rename columns to more convenient names (remove spaces, parentheses, etc.)
    columns_map = {
        'Formatted Date': 'formatted_date',
        'Summary': 'summary',
        'Precip Type': 'precip_type',
        'Temperature (C)': 'temperature',
        'Apparent Temperature (C)': 'apparent_temperature',
        'Humidity': 'humidity',
        'Wind Speed (km/h)': 'wind_speed',
        'Wind Bearing (degrees)': 'wind_bearing',
        'Visibility (km)': 'visibility',
        'Loud Cover': 'loud_cover',
        'Pressure (millibars)': 'pressure',
        'Daily Summary': 'daily_summary'
    }
    
    # Apply the column renaming
    df_cleaned.rename(columns=columns_map, inplace=True)
    
    # Convert date column to datetime with explicit UTC=True to handle mixed timezones
    df_cleaned['date'] = pd.to_datetime(df_cleaned['formatted_date'], utc=True)
    
    # Extract date components for time series analysis
    df_cleaned['year'] = df_cleaned['date'].dt.year
    df_cleaned['month'] = df_cleaned['date'].dt.month
    df_cleaned['day'] = df_cleaned['date'].dt.day
    df_cleaned['hour'] = df_cleaned['date'].dt.hour
    df_cleaned['dayofweek'] = df_cleaned['date'].dt.dayofweek
    df_cleaned['weekofyear'] = df_cleaned['date'].dt.isocalendar().week
    
    # Check for missing values and handle them
    for col in df_cleaned.columns:
        if df_cleaned[col].isna().sum() > 0:
            # For numerical columns, fill with median
            if df_cleaned[col].dtype in ['int64', 'float64']:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
            # For categorical columns, fill with mode
            else:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
    
    # Handle any potential outliers
    numeric_cols = df_cleaned.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        # Skip date columns
        if col in ['year', 'month', 'day', 'hour', 'dayofweek', 'weekofyear']:
            continue
            
        # Calculate IQR
        Q1 = df_cleaned[col].quantile(0.25)
        Q3 = df_cleaned[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Define bounds
        lower_bound = Q1 - 3 * IQR
        upper_bound = Q3 + 3 * IQR
        
        # Cap the outliers
        df_cleaned[col] = df_cleaned[col].clip(lower_bound, upper_bound)
    
    return df_cleaned
```

This function implements several data cleaning steps:
1. Creates a copy of the original DataFrame to avoid modifying it
2. Renames columns to more user-friendly names
3. Converts date strings to proper datetime objects
4. Extracts date components for time-based analysis
5. Handles missing values using appropriate strategies based on data type
6. Detects and mitigates outliers using the Interquartile Range (IQR) method

The function uses a 3×IQR approach for outlier detection, which is more robust than simple standard deviation methods.

## Visualization System

The visualization functionality is implemented in `visualization.py` and includes functions for creating different types of plots.

### Default Style Setup
```python
def set_default_plot_style():
    """Set default plot style for consistency"""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
```
This function establishes a consistent visual style across all plots in the application.

### Time Series Plot Creation
```python
def create_time_series_plot(df, variable, time_agg):
    """
    Create a time series plot for a given variable
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
    variable : str
        The variable to plot
    time_agg : str
        Time aggregation level (Day, Week, Month, Year)
        
    Returns:
    --------
    matplotlib.figure.Figure
        Time series plot
    """
    set_default_plot_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Aggregate data based on selected time level
    if time_agg == "Day":
        df_agg = df.groupby(df['date'].dt.date)[variable].mean().reset_index()
        x_label = "Date"
    elif time_agg == "Week":
        df_agg = df.groupby(['year', 'weekofyear'])[variable].mean().reset_index()
        df_agg['period'] = df_agg['year'].astype(str) + '-W' + df_agg['weekofyear'].astype(str).str.zfill(2)
        x_label = "Year-Week"
    elif time_agg == "Month":
        df_agg = df.groupby(['year', 'month'])[variable].mean().reset_index()
        df_agg['period'] = df_agg['year'].astype(str) + '-' + df_agg['month'].astype(str).str.zfill(2)
        x_label = "Year-Month"
    else:  # Year
        df_agg = df.groupby('year')[variable].mean().reset_index()
        x_label = "Year"
    
    # Plot
    if time_agg == "Day":
        plt.plot(df_agg['date'], df_agg[variable], marker='o', linestyle='-', markersize=4, alpha=0.7)
        plt.gcf().autofmt_xdate()  # Rotate x-axis labels for better readability
    elif time_agg in ["Week", "Month"]:
        plt.plot(range(len(df_agg)), df_agg[variable], marker='o', linestyle='-', markersize=4, alpha=0.7)
        if len(df_agg) > 0:  # Check if there's data to plot
            plt.xticks(range(len(df_agg)), df_agg['period'], rotation=90)
            plt.gca().xaxis.set_major_locator(MaxNLocator(20))  # Show max 20 ticks
    else:  # Year
        plt.plot(df_agg['year'], df_agg[variable], marker='o', linestyle='-', markersize=6)
    
    plt.title(f'Average {variable} by {time_agg}')
    plt.xlabel(x_label)
    plt.ylabel(variable)
    plt.tight_layout()
    
    return fig
```
This function implements time series visualization with flexible time aggregation:
1. Sets up the plot style for consistency
2. Aggregates data based on the selected time level (day, week, month, year)
3. Customizes the plot appearance based on the aggregation level
4. Handles special formatting for date axes and tick labels
5. Limits the number of labels to maintain readability

### Scatter Plot Creation
```python
def create_scatter_plot(df, x_var, y_var):
    """
    Create a scatter plot for two variables
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
    x_var : str
        Variable for x-axis
    y_var : str
        Variable for y-axis
        
    Returns:
    --------
    matplotlib.figure.Figure
        Scatter plot
    """
    set_default_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create scatter plot with a trend line
    sns.regplot(x=x_var, y=y_var, data=df, scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'})
    
    plt.title(f'Relationship between {x_var} and {y_var}')
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.tight_layout()
    
    return fig
```
This function creates scatter plots with regression lines using Seaborn's regplot:
1. Sets the default style for consistency
2. Creates a scatter plot with semi-transparent points (alpha=0.3) to handle overplotting
3. Adds a regression line to visualize the relationship trend
4. Sets appropriate titles and labels

### Correlation Heatmap
```python
def create_heatmap(df, columns):
    """
    Create a correlation heatmap
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
    columns : list
        List of columns to include in the heatmap
        
    Returns:
    --------
    matplotlib.figure.Figure
        Correlation heatmap
    """
    set_default_plot_style()
    
    # Calculate correlation matrix
    corr_matrix = df[columns].corr()
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    sns.heatmap(
        corr_matrix, 
        mask=mask, 
        cmap=cmap, 
        vmax=1, 
        vmin=-1, 
        center=0,
        annot=True, 
        fmt=".2f", 
        square=True, 
        linewidths=.5
    )
    
    plt.title('Correlation Matrix of Weather Variables')
    plt.tight_layout()
    
    return fig
```
This function creates a correlation heatmap with several advanced features:
1. Calculates the correlation matrix for the specified columns
2. Creates a mask to show only the lower triangle (avoiding redundant information)
3. Uses a diverging color palette to clearly show positive vs. negative correlations
4. Annotates each cell with the correlation value
5. Uses a square aspect ratio for clarity

## Analytics Components

The analytics functionality is implemented in `analytics.py` with functions for different types of statistical analysis.

### Basic Statistics Calculation
```python
def calculate_basic_stats(df, columns):
    """
    Calculate basic statistics for numerical columns
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
    columns : list
        List of columns to calculate statistics for
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with basic statistics
    """
    # Calculate statistics
    stats_df = pd.DataFrame({
        'Mean': df[columns].mean(),
        'Median': df[columns].median(),
        'Std Dev': df[columns].std(),
        'Min': df[columns].min(),
        'Max': df[columns].max(),
        'Range': df[columns].max() - df[columns].min(),
        'IQR': df[columns].quantile(0.75) - df[columns].quantile(0.25),
        'Skew': df[columns].skew(),
        'Kurtosis': df[columns].kurt()
    })
    
    return stats_df.round(2)
```
This function calculates several statistical metrics:
1. Central tendency (mean, median)
2. Dispersion (standard deviation, range, IQR)
3. Distribution shape (skewness, kurtosis)
4. Rounds the results to 2 decimal places for readability

### Univariate Analysis
```python
def perform_univariate_analysis(df, variable):
    """
    Perform univariate analysis for a variable
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
    variable : str
        The variable to analyze
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with univariate statistics
    """
    # Calculate percentiles
    percentiles = [0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
    percentile_values = [df[variable].quantile(p) for p in percentiles]
    
    # Calculate statistics
    stats = {
        'Count': df[variable].count(),
        'Missing': df[variable].isna().sum(),
        'Mean': df[variable].mean(),
        'Median': df[variable].median(),
        'Mode': df[variable].mode().iloc[0] if not df[variable].mode().empty else None,
        'Std Dev': df[variable].std(),
        'Variance': df[variable].var(),
        'Min': df[variable].min(),
        'Max': df[variable].max(),
        'Range': df[variable].max() - df[variable].min(),
        'IQR': df[variable].quantile(0.75) - df[variable].quantile(0.25),
        'Skew': df[variable].skew(),
        'Kurtosis': df[variable].kurt()
    }
    
    # Add percentiles to stats
    for p, val in zip(percentiles, percentile_values):
        stats[f'{int(p*100)}th Percentile'] = val
    
    # Convert to DataFrame
    stats_df = pd.DataFrame(list(stats.items()), columns=['Statistic', 'Value'])
    
    return stats_df
```
This function performs a comprehensive univariate analysis:
1. Calculates various percentiles for understanding the distribution
2. Computes a wide range of statistics including measures of central tendency, dispersion, and distribution shape
3. Handles edge cases like empty mode results
4. Returns a formatted DataFrame for display

### Key Questions Analysis
```python
def answer_key_questions(df):
    """
    Answer key questions about the weather data
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
        
    Returns:
    --------
    dict
        Dictionary of questions and answers
    """
    # Initialize dictionary for questions and answers
    qa = {}
    
    # Question 1: What are the seasonal temperature patterns?
    seasonal_temp = df.groupby('month')['temperature'].mean()
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    seasonal_temp.plot(kind='bar', ax=ax1)
    plt.title('Average Temperature by Month')
    plt.xlabel('Month')
    plt.ylabel('Average Temperature (C)')
    plt.tight_layout()
    
    qa["What are the seasonal temperature patterns?"] = {
        'text': f"""
The data shows a clear seasonal pattern in temperature. 
The highest average temperatures occur during the summer months (June-August), 
with the peak in {seasonal_temp.idxmax()} ({seasonal_temp.max():.2f}°C).
The lowest temperatures are in the winter months (December-February),
with the lowest in {seasonal_temp.idxmin()} ({seasonal_temp.min():.2f}°C).
This confirms the expected seasonal variation in the northern hemisphere.
        """,
        'fig': fig1
    }
    
    # [... more questions and analyses ...]
    
    return qa
```
This function implements a structured approach to answering specific meteorological questions:
1. Creates a dictionary to store question-answer pairs
2. For each question, performs relevant calculations and creates appropriate visualizations
3. Formats the results with explanatory text and visualizations
4. Dynamically incorporates calculated values into the explanations

## Reporting System

The reporting functionality is implemented in `reporting.py` with a function to generate comprehensive reports.

### Report Generation
```python
def generate_report(df, columns):
    """
    Generate a comprehensive report based on the data analysis
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
    columns : list
        List of numerical columns used in the analysis
        
    Returns:
    --------
    str
        Markdown formatted report
    """
    # Calculate key statistics
    avg_temp = df['temperature'].mean()
    temp_range = (df['temperature'].min(), df['temperature'].max())
    avg_humidity = df['humidity'].mean() * 100  # Convert to percentage
    
    # Find most common weather summaries
    if 'Summary' in df.columns:
        weather_counts = df['Summary'].value_counts()
        most_common_weather = weather_counts.index[0]
        most_common_pct = weather_counts.iloc[0] / len(df) * 100
    else:
        most_common_weather = "Unknown"
        most_common_pct = 0
    
    # Get date range
    start_date = df['date'].min().strftime('%Y-%m-%d')
    end_date = df['date'].max().strftime('%Y-%m-%d')
    total_days = (df['date'].max() - df['date'].min()).days
    
    # Calculate temperature by season
    df['season'] = (df['month'] % 12 + 3) // 3
    season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    df['season_name'] = df['season'].map(season_map)
    seasonal_temp = df.groupby('season_name')['temperature'].mean().to_dict()
    
    # Calculate correlations
    temp_humidity_corr = df['temperature'].corr(df['humidity'])
    temp_pressure_corr = df['temperature'].corr(df['pressure'])
    temp_wind_corr = df['temperature'].corr(df['windSpeed'])
    
    # Generate markdown report
    report = f"""
## Weather Data Analysis Summary Report

### Dataset Overview
- **Date Range**: {start_date} to {end_date} ({total_days} days)
- **Total Records**: {len(df):,}
- **Variables Analyzed**: {', '.join(columns)}

### Key Findings

#### Temperature Patterns
- **Average Temperature**: {avg_temp:.2f}°C
- **Temperature Range**: {temp_range[0]:.2f}°C to {temp_range[1]:.2f}°C
- **Seasonal Averages**:
  - Winter: {seasonal_temp.get('Winter', 'N/A'):.2f}°C
  - Spring: {seasonal_temp.get('Spring', 'N/A'):.2f}°C
  - Summer: {seasonal_temp.get('Summer', 'N/A'):.2f}°C
  - Fall: {seasonal_temp.get('Fall', 'N/A'):.2f}°C

#### Weather Conditions
- **Average Humidity**: {avg_humidity:.1f}%
- **Most Common Weather**: {most_common_weather} ({most_common_pct:.1f}% of observations)

#### Key Relationships
- **Temperature-Humidity Correlation**: {temp_humidity_corr:.3f}
  - *Interpretation*: {"Strong negative correlation - higher temperatures generally associated with lower humidity" if temp_humidity_corr < -0.5 else "Moderate negative correlation - some tendency for humidity to decrease with temperature" if temp_humidity_corr < -0.3 else "Weak negative correlation" if temp_humidity_corr < 0 else "Strong positive correlation - higher temperatures generally associated with higher humidity" if temp_humidity_corr > 0.5 else "Moderate positive correlation - some tendency for humidity to increase with temperature" if temp_humidity_corr > 0.3 else "Weak positive correlation"}
- **Temperature-Pressure Correlation**: {temp_pressure_corr:.3f}
  - *Interpretation*: {"Strong negative correlation" if temp_pressure_corr < -0.5 else "Moderate negative correlation" if temp_pressure_corr < -0.3 else "Weak negative correlation" if temp_pressure_corr < 0 else "Strong positive correlation" if temp_pressure_corr > 0.5 else "Moderate positive correlation" if temp_pressure_corr > 0.3 else "Weak positive correlation"}
- **Temperature-Wind Speed Correlation**: {temp_wind_corr:.3f}
  - *Interpretation*: {"Strong negative correlation" if temp_wind_corr < -0.5 else "Moderate negative correlation" if temp_wind_corr < -0.3 else "Weak negative correlation" if temp_wind_corr < 0 else "Strong positive correlation" if temp_wind_corr > 0.5 else "Moderate positive correlation" if temp_wind_corr > 0.3 else "Weak positive correlation"}

### Daily Patterns
- Temperature typically reaches its daily minimum in the early morning hours
- Peak temperature usually occurs in the mid-afternoon
- Humidity is generally highest overnight and lowest in the afternoon

### Conclusion
This analysis of weather data reveals clear seasonal and daily patterns in temperature and other variables.
The relationships between different weather variables follow expected meteorological principles,
with notable correlations between temperature, humidity, and other atmospheric conditions.

The dataset provides a comprehensive view of weather patterns over the {total_days}-day period,
showing the typical variations and relationships that characterize the local climate.
    """
    
    return report
```
This function generates a comprehensive markdown-formatted report:
1. Calculates key statistics about the dataset
2. Determines the date range and time span
3. Calculates seasonal temperature averages
4. Computes correlations between key variables
5. Generates interpretive text based on correlation values
6. Assembles all information into a structured markdown report

## Helper Scripts

### Run Script: run.py
```python
#!/usr/bin/env python3
"""
Weather Data Analysis Application Runner

This script provides an easy way to run the Weather Data Analysis application.
It offers options to run different components of the project:
1. Main weather analysis app
2. Project documentation generator
"""

import os
import sys
import subprocess
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Weather Data Analysis Application Runner')
    parser.add_argument('--docs', action='store_true', help='Run the project documentation generator')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the Streamlit application on (default: 5000)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set environment variables
    os.environ['STREAMLIT_SERVER_PORT'] = str(args.port)
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    
    # Check if data file exists
    data_file = "attached_assets/weatherHistory.csv"
    if not os.path.exists(data_file):
        print(f"Error: Data file not found at '{data_file}'")
        print("Please ensure the weather data file is in the correct location.")
        return 1
    
    # Run the appropriate application
    if args.docs:
        print("Starting Project Documentation Generator...")
        cmd = ["streamlit", "run", "project_documentation.py", "--server.port", str(args.port)]
    else:
        print("Starting Weather Data Analysis Application...")
        cmd = ["streamlit", "run", "weather_app.py", "--server.port", str(args.port)]
    
    try:
        print(f"The application will be available at http://localhost:{args.port}")
        print("Press Ctrl+C to stop the application")
        subprocess.run(cmd)
        return 0
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        return 0
    except Exception as e:
        print(f"Error running application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```
This Python script serves as a command-line interface for launching different components of the project:
1. Uses argparse for parsing command-line arguments
2. Sets environment variables for Streamlit configuration
3. Verifies the existence of required data files
4. Launches the appropriate application based on user selection
5. Provides proper error handling and user feedback

### Shell Script: run_weather_analysis.sh
```bash
#!/bin/bash
# Weather Data Analysis Application Runner Script
# This script provides an easy way to start the Weather Data Analysis application

echo "========================================================"
echo "       Weather Data Analysis Application Launcher        "
echo "========================================================"
echo

# Check if data file exists
if [ ! -f "attached_assets/weatherHistory.csv" ]; then
    echo "Error: Weather data file not found!"
    echo "Make sure the file 'weatherHistory.csv' is in the 'attached_assets' directory."
    exit 1
fi

# Function to validate if streamlit is installed
check_streamlit() {
    if ! command -v streamlit &> /dev/null; then
        echo "Streamlit is not installed. Installing required packages..."
        pip install streamlit matplotlib pandas numpy seaborn scipy reportlab
        if [ $? -ne 0 ]; then
            echo "Failed to install required packages. Please install them manually."
            exit 1
        fi
    fi
}

# Function to display menu and get user choice
show_menu() {
    echo "Please select an option:"
    echo "1) Run Weather Data Analysis Application"
    echo "2) Generate PDF Documentation"
    echo "3) Help"
    echo "4) Exit"
    echo
    echo -n "Enter your choice (1-4): "
    read choice
    
    case $choice in
        1)
            run_weather_app
            ;;
        2)
            generate_docs
            ;;
        3)
            show_help
            ;;
        4)
            echo "Exiting. Thank you for using the Weather Data Analysis application!"
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            echo
            show_menu
            ;;
    esac
}

# Function to run the main weather app
run_weather_app() {
    echo
    echo "Starting Weather Data Analysis Application..."
    echo "The application will be available at http://localhost:5000"
    echo "Press Ctrl+C to stop the application"
    streamlit run weather_app.py --server.port 5000 --server.headless true --server.address 0.0.0.0
}

# Function to generate documentation
generate_docs() {
    echo
    echo "Creating comprehensive PDF documentation..."
    echo "Weather data analysis documentation will be saved in the current directory."
    
    # Create a simple Python script to generate the documentation directly
    cat > generate_doc.py << EOF
# [Python code for document generation]
EOF

    # Run the script to generate the documentation
    python generate_doc.py
    
    if [ $? -eq 0 ]; then
        echo "Documentation created successfully!"
        echo "You can find the PDF file: weather_data_analysis_documentation.pdf"
    else
        echo "Error generating documentation. Please check the Python environment."
    fi
    
    echo
    # Return to main menu
    show_menu
}

# Function to display help information
show_help() {
    echo
    echo "Weather Data Analysis Application - Help"
    echo "----------------------------------------"
    echo "This application allows you to analyze historical weather data through"
    echo "statistical analysis and visualizations."
    echo
    echo "Options:"
    echo "  1) Run Weather Analysis App - Starts the main Streamlit application"
    echo "     for analyzing weather data with interactive visualizations."
    echo
    echo "  2) Generate Documentation - Creates a comprehensive PDF documentation"
    echo "     explaining the features and usage of the application."
    echo
    echo "Requirements:"
    echo "  - Python 3.6 or higher"
    echo "  - Streamlit, Pandas, Matplotlib, NumPy, Seaborn, ReportLab packages"
    echo "  - Weather data file in CSV format"
    echo
    echo "For bug reports or feature requests, please contact the developer."
    echo
    
    # Return to main menu
    show_menu
}

# Main script execution
check_streamlit
show_menu
```
This Bash script provides a user-friendly command-line interface:
1. Checks for required data files and dependencies
2. Presents a menu-based interface for selecting operations
3. Handles installation of required packages if they're missing
4. Contains separate functions for different operations
5. Provides helpful error messages and usage information

## Configuration Files

### Streamlit Configuration
The Streamlit configuration is maintained in the `.streamlit/config.toml` file:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

This configuration ensures:
1. The server runs in headless mode, which is appropriate for deployment environments
2. The server binds to all network interfaces (0.0.0.0) making it accessible from other machines
3. The application consistently uses port 5000

## Best Practices and Code Patterns

### Caching for Performance
```python
@st.cache_data
def load_data():
    # Data loading code
    return df
```
The application uses Streamlit's caching mechanism to improve performance. The `@st.cache_data` decorator ensures the data loading function runs only once and caches the results, avoiding redundant operations when the app reruns.

### Error Handling
```python
try:
    df = load_data(file_path)
    df_cleaned = clean_data(df)
    return df_cleaned
except Exception as e:
    st.error(f"Error loading data: {e}")
    return None
```
The code implements proper error handling to catch and report exceptions, providing helpful error messages to users when operations fail.

### Modular Design
The project follows a modular design with separate files for different functionalities:
- `weather_app.py`: Main application logic and UI
- `data_processing.py`: Data loading and cleaning
- `visualization.py`: Visualization functions
- `analytics.py`: Statistical analysis
- `reporting.py`: Report generation

This separation of concerns improves maintainability and makes the codebase easier to understand and extend.

### Docstrings and Comments
```python
def create_box_plot(df, variable, by_month=False):
    """
    Create a box plot for a variable
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
    variable : str
        The variable to plot
    by_month : bool
        Whether to group by month
        
    Returns:
    --------
    matplotlib.figure.Figure
        Box plot
    """
    # Function implementation
```
The code includes comprehensive docstrings that follow the NumPy/SciPy documentation style, clearly explaining function parameters and return values.

### Defensive Programming
```python
# Check if there's data to plot
if len(df_agg) > 0:
    plt.xticks(range(len(df_agg)), df_agg['period'], rotation=90)
    plt.gca().xaxis.set_major_locator(MaxNLocator(20))
```
The code implements defensive programming practices, such as checking for empty DataFrames before attempting to plot them.

## Performance Considerations

### Data Loading Optimization
The application minimizes data loading operations using Streamlit's caching system. This significantly improves performance by avoiding redundant operations during app reruns or user interactions.

### Visualization Efficiency
```python
# Create scatter plot with reduced point transparency to handle overplotting
sns.regplot(x=x_var, y=y_var, data=df, scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'})
```
When working with large datasets, the visualization functions use techniques like transparency (alpha) to handle overplotting and maintain performance.

### Memory Management
```python
# Make a copy to avoid modifying the original dataframe
df_cleaned = df.copy()
```
The application implements careful memory management, creating copies of DataFrames only when necessary to avoid unintended side effects.

### Conditional Processing
```python
# Skip date columns when handling outliers
if col in ['year', 'month', 'day', 'hour', 'dayofweek', 'weekofyear']:
    continue
```
The code uses conditional processing to skip unnecessary operations, improving overall performance.

---

This detailed documentation provides an in-depth look at the code structure, implementation details, and design patterns used in the Weather Data Analysis project. It serves as a comprehensive technical reference for understanding, maintaining, and extending the application.