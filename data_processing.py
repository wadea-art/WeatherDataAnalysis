import pandas as pd
import numpy as np
from datetime import datetime

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
    
    # Rename columns to more convenient names
    df_cleaned.columns = [col.replace(' ', '').replace('(', '').replace(')', '').replace('/', '_') for col in df_cleaned.columns]
    
    # Convert date column to datetime
    df_cleaned['date'] = pd.to_datetime(df_cleaned['FormattedDate'])
    
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
