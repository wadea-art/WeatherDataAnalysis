import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Import custom modules
from data_processing import load_data, clean_data
from visualization import (create_time_series_plot, create_scatter_plot, 
                          create_box_plot, create_heatmap, create_distribution_plot)
from analytics import (calculate_basic_stats, perform_univariate_analysis, 
                      perform_bivariate_analysis, answer_key_questions)
from reporting import generate_report

# Set page configuration
st.set_page_config(
    page_title="Weather Data Analysis",
    page_icon="🌤️",
    layout="wide"
)

# Main title
st.title("🌤️ Weather Data Analysis")
st.subheader("Insights from Historical Weather Data")

# Define file path
file_path = "attached_assets/weatherHistory.csv"

# Load data
@st.cache_data
def get_data():
    try:
        df = load_data(file_path)
        df_cleaned = clean_data(df)
        return df_cleaned
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Loading data message
with st.spinner("Loading and processing data..."):
    df = get_data()

if df is not None:
    # Display data overview
    st.subheader("Data Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Total Records: {df.shape[0]:,}")
        st.write(f"Time Range: {df['date'].min().date()} to {df['date'].max().date()}")
    
    with col2:
        st.write(f"Features: {df.shape[1]}")
        st.write(f"Missing Values: {df.isna().sum().sum():,}")
    
    # Show sample data
    with st.expander("View Sample Data"):
        st.dataframe(df.head(10))
    
    # Show data types and info
    with st.expander("Data Types and Information"):
        # Create a string representation of dataframe info
        info_str = f"DataFrame has {df.shape[0]} rows and {df.shape[1]} columns\n\n"
        info_str += "Data types:\n"
        for col, dtype in df.dtypes.items():
            info_str += f"  {col}: {dtype}\n"
        st.text(info_str)
    
    # Basic statistics
    st.subheader("Basic Statistics")
    
    # Select relevant numerical columns for statistics
    numerical_cols = ['temperature', 'apparent_temperature', 'humidity', 
                      'wind_speed', 'wind_bearing', 'visibility', 'pressure']
    
    stats_df = calculate_basic_stats(df, numerical_cols)
    st.dataframe(stats_df)
    
    # Data Analysis Section
    st.header("Data Analysis")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Time Series Analysis", 
        "Univariate Analysis", 
        "Bivariate Analysis", 
        "Key Questions",
        "Report Summary"
    ])
    
    # Time Series Analysis
    with tab1:
        st.subheader("Time Series Analysis")
        
        # Time aggregation option
        time_agg = st.selectbox(
            "Select time aggregation",
            ["Day", "Week", "Month", "Year"]
        )
        
        # Variable selection
        ts_var = st.selectbox(
            "Select variable to analyze over time",
            numerical_cols
        )
        
        # Generate time series plot
        fig = create_time_series_plot(df, ts_var, time_agg)
        st.pyplot(fig)
        
        # Daily patterns
        st.subheader("Daily Patterns")
        daily_var = st.selectbox(
            "Select variable to analyze by hour",
            numerical_cols,
            key="daily_var"
        )
        
        fig = plt.figure(figsize=(10, 6))
        sns.lineplot(x='hour', y=daily_var, data=df, marker='o')
        plt.title(f'Average {daily_var} by Hour of Day')
        plt.xlabel('Hour of Day')
        plt.ylabel(daily_var)
        plt.grid(True, alpha=0.3)
        st.pyplot(fig)
        
    # Univariate Analysis
    with tab2:
        st.subheader("Univariate Analysis")
        
        # Variable selection for univariate analysis
        uni_var = st.selectbox(
            "Select variable to analyze",
            numerical_cols
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution plot
            fig = create_distribution_plot(df, uni_var)
            st.pyplot(fig)
            
        with col2:
            # Box plot
            fig = create_box_plot(df, uni_var)
            st.pyplot(fig)
        
        # Univariate statistics
        uni_stats = perform_univariate_analysis(df, uni_var)
        st.dataframe(uni_stats)
        
    # Bivariate Analysis
    with tab3:
        st.subheader("Bivariate Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Variable selection for X
            x_var = st.selectbox(
                "Select X variable",
                numerical_cols
            )
        
        with col2:
            # Variable selection for Y
            y_var = st.selectbox(
                "Select Y variable",
                [col for col in numerical_cols if col != x_var]
            )
        
        # Create scatter plot
        fig = create_scatter_plot(df, x_var, y_var)
        st.pyplot(fig)
        
        # Calculate correlation
        corr = df[x_var].corr(df[y_var])
        corr_value = corr if not pd.isna(corr) else 0
        st.write(f"Correlation between {x_var} and {y_var}: **{corr_value:.4f}**")
        
        # Correlation heatmap
        st.subheader("Correlation Matrix")
        fig = create_heatmap(df, numerical_cols)
        st.pyplot(fig)
        
        # Perform bivariate analysis
        bi_stats = perform_bivariate_analysis(df, numerical_cols)
        with st.expander("View Correlation Analysis"):
            st.dataframe(bi_stats)
    
    # Key Questions
    with tab4:
        st.subheader("Key Weather Questions")
        
        # Generate answers to key questions
        questions_answers = answer_key_questions(df)
        
        for i, (question, answer) in enumerate(questions_answers.items()):
            with st.expander(question):
                st.write(answer['text'])
                if 'fig' in answer:
                    st.pyplot(answer['fig'])
    
    # Report Summary
    with tab5:
        st.subheader("Weather Data Analysis Report")
        
        # Generate comprehensive report
        report = generate_report(df, numerical_cols)
        st.markdown(report)

else:
    st.error("Failed to load data. Please check the file path and try again.")
