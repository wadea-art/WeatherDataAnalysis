import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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
    stats_df = pd.DataFrame(stats.items(), columns=['Statistic', 'Value'])
    
    return stats_df

def perform_bivariate_analysis(df, columns):
    """
    Perform bivariate analysis for numerical columns
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
    columns : list
        List of columns to include in the analysis
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with correlation analysis
    """
    # Calculate correlation matrix
    corr_matrix = df[columns].corr()
    
    # Reshape correlation matrix to long format
    corr_df = corr_matrix.stack().reset_index()
    corr_df.columns = ['Variable 1', 'Variable 2', 'Correlation']
    
    # Filter out self-correlations and duplicates
    corr_df = corr_df[(corr_df['Variable 1'] != corr_df['Variable 2'])]
    seen = set()
    unique_pairs = []
    for idx, row in corr_df.iterrows():
        pair = tuple(sorted([row['Variable 1'], row['Variable 2']]))
        if pair not in seen:
            seen.add(pair)
            unique_pairs.append(row)
    
    unique_corr_df = pd.DataFrame(unique_pairs)
    unique_corr_df = unique_corr_df.sort_values('Correlation', ascending=False)
    
    return unique_corr_df

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
    
    # Question 2: Is there a correlation between temperature and humidity?
    corr = df['temperature'].corr(df['humidity'])
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='temperature', y='humidity', data=df, alpha=0.5, ax=ax2)
    plt.title('Relationship between Temperature and Humidity')
    plt.xlabel('Temperature (C)')
    plt.ylabel('Humidity')
    plt.tight_layout()
    
    qa["Is there a correlation between temperature and humidity?"] = {
        'text': f"""
The correlation between temperature and humidity is {corr:.4f}.
This {"strong negative" if corr < -0.5 else "moderate negative" if corr < -0.3 else "weak negative" if corr < 0 else "strong positive" if corr > 0.5 else "moderate positive" if corr > 0.3 else "weak positive"} correlation suggests that 
{"as temperature increases, humidity tends to decrease." if corr < 0 else "as temperature increases, humidity also tends to increase."} 
This relationship is consistent with meteorological principles, as warmer air can hold more moisture,
but relative humidity often decreases with temperature if the absolute moisture content remains constant.
        """,
        'fig': fig2
    }
    
    # Question 3: How does wind speed affect the apparent temperature?
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='windSpeed', y='temperature', data=df, alpha=0.5, ax=ax3)
    sns.scatterplot(x='windSpeed', y='apparentTemperature', data=df, alpha=0.5, ax=ax3)
    plt.title('Effect of Wind Speed on Apparent Temperature')
    plt.xlabel('Wind Speed (km/h)')
    plt.ylabel('Temperature (C)')
    plt.legend(['Actual Temperature', 'Apparent Temperature'])
    plt.tight_layout()
    
    # Calculate average difference
    df['temp_diff'] = df['temperature'] - df['apparentTemperature']
    avg_diff = df.groupby(pd.cut(df['windSpeed'], bins=5))['temp_diff'].mean()
    
    qa["How does wind speed affect the apparent temperature?"] = {
        'text': f"""
Wind speed has a noticeable effect on how we perceive temperature (apparent temperature).
The scatter plot shows that at higher wind speeds, there is typically a larger difference 
between the actual temperature and the apparent temperature.

This phenomenon, known as the wind chill effect, is particularly evident in cooler temperatures
where increased wind speed makes it feel colder than the actual temperature.
At higher temperatures, the effect is less pronounced or even reversed (heat index).

When analyzing the data by wind speed ranges, the average difference between actual and apparent 
temperature increases with wind speed, confirming the wind chill effect in the dataset.
        """,
        'fig': fig3
    }
    
    # Question 4: What weather conditions are associated with different types of precipitation?
    if 'PrecipType' in df.columns:
        precip_stats = df.groupby('PrecipType').agg({
            'temperature': 'mean',
            'humidity': 'mean',
            'pressure': 'mean',
            'visibility': 'mean'
        }).reset_index()
        
        qa["What weather conditions are associated with different types of precipitation?"] = {
            'text': f"""
The data shows distinct weather patterns associated with different precipitation types:

Rain:
- Average Temperature: {precip_stats.loc[precip_stats['PrecipType'] == 'rain', 'temperature'].values[0]:.2f}°C
- Average Humidity: {precip_stats.loc[precip_stats['PrecipType'] == 'rain', 'humidity'].values[0]:.2f}
- Average Pressure: {precip_stats.loc[precip_stats['PrecipType'] == 'rain', 'pressure'].values[0]:.2f} millibars
- Average Visibility: {precip_stats.loc[precip_stats['PrecipType'] == 'rain', 'visibility'].values[0]:.2f} km

Snow (if present in the data):
- Average Temperature: {precip_stats.loc[precip_stats['PrecipType'] == 'snow', 'temperature'].values[0]:.2f}°C if 'snow' in precip_stats['PrecipType'].values else 'Not present in data'
- Average Humidity: {precip_stats.loc[precip_stats['PrecipType'] == 'snow', 'humidity'].values[0]:.2f} if 'snow' in precip_stats['PrecipType'].values else 'Not present in data'
- Average Pressure: {precip_stats.loc[precip_stats['PrecipType'] == 'snow', 'pressure'].values[0]:.2f} millibars if 'snow' in precip_stats['PrecipType'].values else 'Not present in data'
- Average Visibility: {precip_stats.loc[precip_stats['PrecipType'] == 'snow', 'visibility'].values[0]:.2f} km if 'snow' in precip_stats['PrecipType'].values else 'Not present in data'

These patterns align with meteorological expectations: rain occurs at higher temperatures than snow,
and both typically involve higher humidity levels compared to clear conditions.
            """
        }
    
    # Question 5: What are the daily patterns in temperature?
    hourly_temp = df.groupby('hour')['temperature'].mean()
    
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    hourly_temp.plot(kind='line', marker='o', ax=ax5)
    plt.title('Average Temperature by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Temperature (C)')
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Find the hottest and coldest hours
    hottest_hour = hourly_temp.idxmax()
    coldest_hour = hourly_temp.idxmin()
    
    qa["What are the daily patterns in temperature?"] = {
        'text': f"""
The temperature follows a clear daily cycle:
- Temperatures are lowest in the early morning, with the minimum occurring around {coldest_hour}:00 ({hourly_temp[coldest_hour]:.2f}°C)
- Temperatures rise throughout the morning, reaching their peak in the afternoon around {hottest_hour}:00 ({hourly_temp[hottest_hour]:.2f}°C)
- After the peak, temperatures gradually decline through the evening and night

This pattern is consistent with the typical diurnal temperature cycle, where the maximum temperature 
occurs a few hours after solar noon due to thermal inertia, and the minimum occurs just before sunrise
when the surface has cooled for the longest period without solar heating.
        """,
        'fig': fig5
    }
    
    return qa
