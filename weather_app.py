import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Weather Data Analysis",
    page_icon="🌤️",
    layout="wide"
)

# Main title
st.title("🌤️ Weather Data Analysis")
st.subheader("Insights from Historical Weather Data")

# Load and process data
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

# Load the data
with st.spinner("Loading data..."):
    df = load_data()

if df is not None:
    # Data Overview
    st.header("1. Data Overview")
    
    # Basic information about the dataset
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Total Records:** {df.shape[0]:,}")
        st.write(f"**Time Range:** {df['date'].min().date()} to {df['date'].max().date()}")
    
    with col2:
        st.write(f"**Features:** {df.shape[1]}")
        num_missing = df.isna().sum().sum()
        st.write(f"**Missing Values:** {num_missing:,}")
    
    # Show sample data
    with st.expander("View Sample Data"):
        st.dataframe(df.head(10))
    
    # 2. Basic Statistics
    st.header("2. Basic Statistics")
    
    # Select numerical columns for analysis
    numerical_cols = ['temperature', 'apparent_temp', 'humidity', 
                      'wind_speed', 'wind_bearing', 'visibility', 'pressure']
    
    # Calculate basic statistics
    stats_df = pd.DataFrame({
        'Mean': df[numerical_cols].mean(),
        'Median': df[numerical_cols].median(),
        'Min': df[numerical_cols].min(),
        'Max': df[numerical_cols].max(),
        'Std Dev': df[numerical_cols].std()
    }).round(2)
    
    st.dataframe(stats_df)
    
    # 3. Univariate Analysis
    st.header("3. Univariate Analysis")
    
    # Select a variable for analysis
    selected_var = st.selectbox("Select a variable to analyze:", numerical_cols)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram with KDE
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.histplot(df[selected_var], kde=True, ax=ax1)
        ax1.set_title(f'Distribution of {selected_var}')
        ax1.set_xlabel(selected_var)
        ax1.set_ylabel('Frequency')
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)
    
    with col2:
        # Box plot
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.boxplot(y=df[selected_var], ax=ax2)
        ax2.set_title(f'Box Plot of {selected_var}')
        ax2.set_ylabel(selected_var)
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)
    
    # Additional statistics for the selected variable
    with st.expander("Detailed Statistics"):
        q1 = df[selected_var].quantile(0.25)
        q3 = df[selected_var].quantile(0.75)
        iqr = q3 - q1
        
        stats = {
            'Count': df[selected_var].count(),
            'Mean': df[selected_var].mean(),
            'Median': df[selected_var].median(),
            'Mode': df[selected_var].mode().iloc[0] if not df[selected_var].mode().empty else None,
            'Standard Deviation': df[selected_var].std(),
            'Minimum': df[selected_var].min(),
            'Maximum': df[selected_var].max(),
            'Range': df[selected_var].max() - df[selected_var].min(),
            '25th Percentile (Q1)': q1,
            '75th Percentile (Q3)': q3,
            'IQR': iqr,
            'Skewness': df[selected_var].skew(),
            'Kurtosis': df[selected_var].kurt()
        }
        
        st.table(pd.DataFrame([stats], index=['Value']).T)
    
    # 4. Time Series Analysis
    st.header("4. Time Series Trends")
    
    # Time aggregation selection
    time_agg = st.selectbox("Select time aggregation level:", ["Day", "Month", "Year"])
    ts_var = st.selectbox("Select variable to analyze over time:", numerical_cols, key="ts_var")
    
    # Aggregate data based on time level
    if time_agg == "Day":
        df_agg = df.groupby(df['date'].dt.date)[ts_var].mean().reset_index()
        x_col = 'date'
        title = f'Average {ts_var} by Day'
    elif time_agg == "Month":
        df_agg = df.groupby([df['year'], df['month']])[ts_var].mean().reset_index()
        df_agg['period'] = df_agg['year'].astype(str) + '-' + df_agg['month'].astype(str).str.zfill(2)
        x_col = 'period'
        title = f'Average {ts_var} by Month'
    else:  # Year
        df_agg = df.groupby('year')[ts_var].mean().reset_index()
        x_col = 'year'
        title = f'Average {ts_var} by Year'
    
    # Create time series plot
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    
    if time_agg == "Day":
        plt.plot(df_agg[x_col], df_agg[ts_var], marker='o', linestyle='-', markersize=4, alpha=0.7)
        plt.gcf().autofmt_xdate()  # Rotate date labels
    else:
        plt.plot(range(len(df_agg)), df_agg[ts_var], marker='o', linestyle='-', markersize=4, alpha=0.7)
        plt.xticks(range(len(df_agg)), df_agg[x_col], rotation=90)
    
    plt.title(title)
    plt.xlabel(time_agg)
    plt.ylabel(ts_var)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    st.pyplot(fig3)
    
    # Daily patterns
    st.subheader("Daily Patterns")
    hourly_var = st.selectbox("Select variable to analyze by hour of day:", numerical_cols, key="hourly_var")
    
    # Aggregate by hour
    hourly_data = df.groupby('hour')[hourly_var].mean().reset_index()
    
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    plt.plot(hourly_data['hour'], hourly_data[hourly_var], marker='o', linestyle='-')
    plt.title(f'Average {hourly_var} by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel(hourly_var)
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    st.pyplot(fig4)
    
    # 5. Bivariate Analysis
    st.header("5. Bivariate Analysis")
    
    # Variable selection for scatter plot
    col1, col2 = st.columns(2)
    
    with col1:
        x_var = st.selectbox("Select X variable:", numerical_cols, key="x_var")
    
    with col2:
        y_var = st.selectbox("Select Y variable:", [col for col in numerical_cols if col != x_var], key="y_var")
    
    # Create scatter plot
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=x_var, y=y_var, data=df, alpha=0.5, ax=ax5)
    sns.regplot(x=x_var, y=y_var, data=df, scatter=False, ax=ax5, color='red')
    
    plt.title(f'Relationship between {x_var} and {y_var}')
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    st.pyplot(fig5)
    
    # Calculate correlation
    correlation = df[x_var].corr(df[y_var])
    st.write(f"**Correlation coefficient:** {correlation:.4f}")
    
    # Correlation heatmap
    st.subheader("Correlation Matrix")
    
    corr_matrix = df[numerical_cols].corr().round(2)
    
    fig6, ax6 = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    heatmap = sns.heatmap(
        corr_matrix, 
        mask=mask, 
        annot=True, 
        cmap=cmap, 
        vmax=1, 
        vmin=-1, 
        center=0,
        square=True, 
        linewidths=.5,
        fmt=".2f",
        ax=ax6
    )
    
    plt.title('Correlation Matrix of Weather Variables')
    plt.tight_layout()
    
    st.pyplot(fig6)
    
    # 6. Key Questions
    st.header("6. Key Questions to Explore")
    
    # Question 1: Seasonal temperature patterns
    with st.expander("What are the seasonal temperature patterns?"):
        # Aggregate by month
        monthly_temp = df.groupby('month')['temperature'].mean().reset_index()
        
        fig7, ax7 = plt.subplots(figsize=(10, 6))
        plt.bar(monthly_temp['month'], monthly_temp['temperature'])
        plt.title('Average Temperature by Month')
        plt.xlabel('Month')
        plt.ylabel('Temperature (C)')
        plt.xticks(range(1, 13))
        plt.grid(True, alpha=0.3)
        
        st.pyplot(fig7)
        
        # Analysis text
        hottest_month = monthly_temp.loc[monthly_temp['temperature'].idxmax()]
        coldest_month = monthly_temp.loc[monthly_temp['temperature'].idxmin()]
        
        st.write(f"""
        The data shows a clear seasonal pattern in temperature:
        
        - Highest temperature: Month {int(hottest_month['month'])} ({hottest_month['temperature']:.2f}°C)
        - Lowest temperature: Month {int(coldest_month['month'])} ({coldest_month['temperature']:.2f}°C)
        
        This pattern aligns with typical seasonal variations, with warmer temperatures in summer months 
        and cooler temperatures in winter months.
        """)
    
    # Question 2: Relationship between temperature and humidity
    with st.expander("How does temperature relate to humidity?"):
        fig8, ax8 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='temperature', y='humidity', data=df, alpha=0.5, ax=ax8)
        sns.regplot(x='temperature', y='humidity', data=df, scatter=False, ax=ax8, color='red')
        
        plt.title('Relationship between Temperature and Humidity')
        plt.xlabel('Temperature (C)')
        plt.ylabel('Humidity')
        plt.grid(True, alpha=0.3)
        
        st.pyplot(fig8)
        
        temp_humid_corr = df['temperature'].corr(df['humidity'])
        
        st.write(f"""
        The correlation between temperature and humidity is {temp_humid_corr:.4f}.
        
        This {"strong negative" if temp_humid_corr < -0.5 else "moderate negative" if temp_humid_corr < -0.3 else "weak negative" if temp_humid_corr < 0 else "strong positive" if temp_humid_corr > 0.5 else "moderate positive" if temp_humid_corr > 0.3 else "weak positive"} correlation suggests that 
        {"as temperature increases, humidity tends to decrease." if temp_humid_corr < 0 else "as temperature increases, humidity also tends to increase."}
        
        This relationship is consistent with weather patterns, as warmer air can hold more moisture,
        but relative humidity often decreases with temperature if the absolute moisture content remains constant.
        """)
    
    # Question 3: Effect of wind speed on apparent temperature
    with st.expander("How does wind speed affect the apparent temperature?"):
        fig9, ax9 = plt.subplots(figsize=(10, 6))
        
        # Scatter plot with two variables
        plt.scatter(df['wind_speed'], df['temperature'], alpha=0.3, label='Actual Temperature')
        plt.scatter(df['wind_speed'], df['apparent_temp'], alpha=0.3, label='Apparent Temperature')
        
        plt.title('Effect of Wind Speed on Apparent Temperature')
        plt.xlabel('Wind Speed (km/h)')
        plt.ylabel('Temperature (C)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        st.pyplot(fig9)
        
        # Calculate difference based on wind speed
        df['temp_diff'] = df['temperature'] - df['apparent_temp']
        
        # Create wind speed categories
        wind_cats = pd.cut(df['wind_speed'], bins=5)
        diff_by_wind = df.groupby(wind_cats)['temp_diff'].mean()
        
        st.write(f"""
        The data shows that wind speed affects how we perceive temperature:
        
        At higher wind speeds, the difference between actual and apparent temperature tends to increase,
        which demonstrates the 'wind chill' effect. This is particularly evident in cooler temperatures
        where wind makes it feel colder than the actual air temperature.
        
        The average temperature difference by wind speed range:
        """)
        
        st.table(diff_by_wind.to_frame("Average Difference (C)").round(2))
    
    # 7. Reporting - Summary of findings
    st.header("8. Summary of Findings")
    
    # Generate the report
    avg_temp = df['temperature'].mean()
    temp_range = (df['temperature'].min(), df['temperature'].max())
    avg_humidity = df['humidity'].mean() * 100  # Convert to percentage
    
    # Most common weather
    if 'summary' in df.columns:
        weather_counts = df['summary'].value_counts()
        most_common_weather = weather_counts.index[0]
        weather_percentage = (weather_counts.iloc[0] / len(df)) * 100
    else:
        most_common_weather = "Unknown"
        weather_percentage = 0
    
    # Date range
    start_date = df['date'].min().strftime('%Y-%m-%d')
    end_date = df['date'].max().strftime('%Y-%m-%d')
    
    # Create the report content
    report_content = f"""
    # Weather Data Analysis Summary Report
    
    ## Dataset Overview
    - **Date Range**: {start_date} to {end_date}
    - **Total Records**: {len(df):,}
    
    ## Key Findings
    
    ### Temperature Patterns
    - **Average Temperature**: {avg_temp:.2f}°C
    - **Temperature Range**: {temp_range[0]:.2f}°C to {temp_range[1]:.2f}°C
    
    ### Weather Conditions
    - **Average Humidity**: {avg_humidity:.1f}%
    - **Most Common Weather**: {most_common_weather} ({weather_percentage:.1f}% of observations)
    
    ### Key Relationships
    - **Temperature-Humidity Correlation**: {df['temperature'].corr(df['humidity']):.3f}
    - **Temperature-Pressure Correlation**: {df['temperature'].corr(df['pressure']):.3f}
    - **Temperature-Wind Speed Correlation**: {df['temperature'].corr(df['wind_speed']):.3f}
    
    ### Daily Patterns
    - Temperature typically reaches its daily minimum in the early morning hours
    - Peak temperature usually occurs in the mid-afternoon
    - Humidity is generally highest overnight and lowest in the afternoon
    
    ## Conclusion
    This analysis reveals clear seasonal and daily patterns in temperature and other variables.
    The relationships between different weather variables follow expected meteorological principles,
    with notable correlations between temperature, humidity, and other atmospheric conditions.
    """
    
    # Display report in the app
    st.markdown(report_content)
    
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
        
        # Split by lines
        lines = report_text.strip().split("\n")
        current_list = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_list:
                    elements.append(Paragraph("<br/>".join(current_list), styles["Normal"]))
                    current_list = []
                elements.append(Spacer(1, 0.1*inch))
            elif line.startswith("# "):
                if current_list:
                    elements.append(Paragraph("<br/>".join(current_list), styles["Normal"]))
                    current_list = []
                elements.append(Paragraph(line[2:], title_style))
            elif line.startswith("## "):
                if current_list:
                    elements.append(Paragraph("<br/>".join(current_list), styles["Normal"]))
                    current_list = []
                elements.append(Paragraph(line[3:], styles["Heading2"]))
            elif line.startswith("### "):
                if current_list:
                    elements.append(Paragraph("<br/>".join(current_list), styles["Normal"]))
                    current_list = []
                elements.append(Paragraph(line[4:], styles["Heading3"]))
            elif line.startswith("- "):
                # Convert markdown list items to HTML list items
                current_list.append(f"• {line[2:]}")
            else:
                if current_list:
                    elements.append(Paragraph("<br/>".join(current_list), styles["Normal"]))
                    current_list = []
                elements.append(Paragraph(line, styles["Normal"]))
        
        # Add any remaining list items
        if current_list:
            elements.append(Paragraph("<br/>".join(current_list), styles["Normal"]))
        
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

else:
    st.error("Failed to load data. Please check the file path and try again.")