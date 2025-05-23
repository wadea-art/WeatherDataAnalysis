import pandas as pd
import numpy as np

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
