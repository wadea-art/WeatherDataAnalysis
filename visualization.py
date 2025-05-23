import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def set_default_plot_style():
    """Set default plot style for consistency"""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3

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
        df_agg = df.groupby([df['date'].dt.year, df['date'].dt.month])[variable].mean().reset_index()
        df_agg['period'] = df_agg['date_year'].astype(str) + '-' + df_agg['date_month'].astype(str).str.zfill(2)
        x_label = "Year-Month"
    else:  # Year
        df_agg = df.groupby(df['date'].dt.year)[variable].mean().reset_index()
        x_label = "Year"
    
    # Plot
    if time_agg == "Day":
        plt.plot(df_agg['date'], df_agg[variable], marker='o', linestyle='-', markersize=4, alpha=0.7)
        plt.gcf().autofmt_xdate()  # Rotate x-axis labels for better readability
    elif time_agg in ["Week", "Month"]:
        plt.plot(range(len(df_agg)), df_agg[variable], marker='o', linestyle='-', markersize=4, alpha=0.7)
        plt.xticks(range(len(df_agg)), df_agg['period'], rotation=90)
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))  # Show max 20 ticks
    else:  # Year
        plt.plot(df_agg['date_year'], df_agg[variable], marker='o', linestyle='-', markersize=6)
    
    plt.title(f'Average {variable} by {time_agg}')
    plt.xlabel(x_label)
    plt.ylabel(variable)
    plt.tight_layout()
    
    return fig

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
    set_default_plot_style()
    fig, ax = plt.subplots(figsize=(12 if by_month else 8, 6))
    
    if by_month:
        # Create box plot by month
        sns.boxplot(x='month', y=variable, data=df)
        plt.title(f'Distribution of {variable} by Month')
        plt.xlabel('Month')
    else:
        # Create a single box plot
        sns.boxplot(y=variable, data=df)
        plt.title(f'Distribution of {variable}')
    
    plt.ylabel(variable)
    plt.tight_layout()
    
    return fig

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

def create_distribution_plot(df, variable):
    """
    Create a distribution plot for a variable
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned weather data
    variable : str
        The variable to plot
        
    Returns:
    --------
    matplotlib.figure.Figure
        Distribution plot
    """
    set_default_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create distribution plot
    sns.histplot(df[variable], kde=True)
    
    plt.title(f'Distribution of {variable}')
    plt.xlabel(variable)
    plt.ylabel('Frequency')
    plt.tight_layout()
    
    return fig
