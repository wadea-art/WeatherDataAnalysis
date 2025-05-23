import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib import colors
import streamlit as st

def generate_project_documentation():
    """
    Generate a detailed PDF documentation about the Weather Data Analysis project
    """
    # Create an in-memory buffer
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                          rightMargin=0.5*inch, leftMargin=0.5*inch,
                          topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    # Create custom styles with unique names to avoid conflicts
    doc_title_style = ParagraphStyle(name='DocTitleStyle', 
                                 parent=styles['Heading1'], 
                                 fontSize=20, 
                                 alignment=TA_CENTER,
                                 spaceAfter=16)
    doc_heading2_style = ParagraphStyle(name='DocHeading2Style', 
                                parent=styles['Heading2'], 
                                fontSize=16, 
                                spaceAfter=12)
    doc_heading3_style = ParagraphStyle(name='DocHeading3Style', 
                                parent=styles['Heading3'], 
                                fontSize=14, 
                                spaceAfter=10)
    doc_normal_style = ParagraphStyle(name='DocNormalStyle', 
                                  parent=styles['Normal'], 
                                  alignment=TA_JUSTIFY,
                                  spaceAfter=8)
    
    # Define all content elements
    elements = []
    
    # Title
    elements.append(Paragraph("Weather Data Analysis Project", doc_title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Introduction
    elements.append(Paragraph("1. Introduction", doc_heading2_style))
    intro_text = """
    This document provides a comprehensive overview of the Weather Data Analysis project, which is designed
    to analyze historical weather data and extract meaningful insights through statistical analysis and 
    data visualization. The application enables users to explore temperature patterns, correlations between 
    weather variables, and seasonal trends from a comprehensive weather dataset.
    """
    elements.append(Paragraph(intro_text, doc_normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Project Overview
    elements.append(Paragraph("2. Project Overview", doc_heading2_style))
    overview_text = """
    The Weather Data Analysis application is a Streamlit-based web application that processes and analyzes
    historical weather data. It provides interactive visualizations and statistical analysis to help users
    understand weather patterns, correlations between different meteorological variables, and seasonal trends.
    
    The application is designed to be user-friendly, allowing for interactive exploration of the data through
    various visualizations and analysis techniques. Users can select specific variables, time periods, and 
    analysis methods to customize their exploration of the weather data.
    """
    elements.append(Paragraph(overview_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # Features
    elements.append(Paragraph("3. Features", styles['Heading2']))
    elements.append(Paragraph("The application includes the following key features:", styles['Normal']))
    
    # 3.1 Data Overview
    elements.append(Paragraph("3.1 Data Overview", styles['Heading3']))
    data_overview_text = """
    This section provides basic information about the dataset, including:
    
    • Total number of records in the dataset
    • Time range covered by the data
    • Number of features (variables) in the dataset
    • Summary of missing values
    
    Users can also view a sample of the raw data and information about data types to better understand
    the structure of the dataset. This helps establish context for the subsequent analyses.
    """
    elements.append(Paragraph(data_overview_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # 3.2 Basic Statistics
    elements.append(Paragraph("3.2 Basic Statistics", styles['Heading3']))
    basic_stats_text = """
    This feature calculates and displays fundamental statistical measures for key numerical variables in 
    the weather dataset, including:
    
    • Mean (average) values
    • Median values
    • Minimum and maximum values
    • Standard deviation
    
    These statistics provide a quantitative summary of the central tendency, spread, and range of each
    weather variable, giving users an immediate sense of the data distribution before diving into
    more detailed analyses.
    """
    elements.append(Paragraph(basic_stats_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # 3.3 Univariate Analysis
    elements.append(Paragraph("3.3 Univariate Analysis", styles['Heading3']))
    univariate_text = """
    The univariate analysis feature allows users to explore individual weather variables in depth:
    
    • Interactive selection of any weather variable for analysis
    • Histogram with kernel density estimation (KDE) showing the distribution of values
    • Box plot displaying the median, quartiles, and potential outliers
    • Detailed statistics including percentiles, skewness, and kurtosis
    
    This section helps users understand the distribution characteristics of each variable, identify
    potential outliers, and assess the normality of the data, which is crucial for selecting appropriate
    statistical methods for further analysis.
    """
    elements.append(Paragraph(univariate_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # 3.4 Time Series Trends
    elements.append(Paragraph("3.4 Time Series Trends", styles['Heading3']))
    time_series_text = """
    This feature focuses on analyzing how weather variables change over time:
    
    • User-selectable time aggregation levels (day, month, year)
    • Interactive selection of the weather variable to analyze
    • Time series plots showing trends and patterns over the selected time scale
    • Daily patterns analysis showing how variables change throughout the day
    
    The time series analysis helps identify seasonal patterns, long-term trends, and cyclical
    variations in weather conditions. The daily patterns analysis is particularly useful for
    understanding diurnal cycles in temperature, humidity, and other variables.
    """
    elements.append(Paragraph(time_series_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # 3.5 Bivariate Analysis
    elements.append(Paragraph("3.5 Bivariate Analysis", styles['Heading3']))
    bivariate_text = """
    The bivariate analysis feature examines relationships between pairs of weather variables:
    
    • Interactive selection of X and Y variables for comparison
    • Scatter plots with regression lines to visualize relationships
    • Calculation of correlation coefficients to quantify relationship strength
    • Correlation heatmap showing relationships among all numerical variables
    
    This analysis helps identify dependencies and correlations between different weather parameters,
    such as how temperature relates to humidity or how wind speed affects apparent temperature.
    Understanding these relationships is essential for weather forecasting and climate modeling.
    """
    elements.append(Paragraph(bivariate_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # 3.6 Key Questions Exploration
    elements.append(Paragraph("3.6 Key Questions Exploration", styles['Heading3']))
    key_questions_text = """
    This feature provides in-depth analyses of specific weather-related questions:
    
    • Seasonal temperature patterns analysis with monthly averages
    • Investigation of the relationship between temperature and humidity
    • Analysis of how wind speed affects apparent temperature
    • Exploration of weather conditions associated with different precipitation types
    
    Each question is addressed through both visualizations and explanatory text, providing
    insights into important meteorological phenomena. These analyses demonstrate practical
    applications of the data and help users understand complex weather interactions.
    """
    elements.append(Paragraph(key_questions_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # 3.7 Summary Report
    elements.append(Paragraph("3.7 Summary Report", styles['Heading3']))
    summary_report_text = """
    The summary report feature consolidates key findings and insights:
    
    • Overview of the dataset scope and characteristics
    • Summary of temperature patterns and ranges
    • Overview of prevalent weather conditions
    • Summary of key correlations between weather variables
    • Downloadable PDF report with all key findings
    
    This section serves as a comprehensive summary of the analyses, presenting the most important
    insights in a clear, organized format. The PDF download functionality allows users to save
    and share the findings for reference or presentation purposes.
    """
    elements.append(Paragraph(summary_report_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Technical Details
    elements.append(Paragraph("4. Technical Implementation", styles['Heading2']))
    tech_details_text = """
    The Weather Data Analysis application is built using several key technologies and libraries:
    
    • Python as the primary programming language
    • Streamlit for creating the interactive web application interface
    • Pandas for data manipulation and analysis
    • Matplotlib and Seaborn for data visualization
    • NumPy for numerical computations
    • ReportLab for generating PDF reports
    
    The application follows a modular structure with separate components handling different aspects
    of the data analysis pipeline:
    
    1. Data Loading and Cleaning: Handles reading the CSV file, converting date formats, and 
       preprocessing the data for analysis
    2. Statistical Analysis: Calculates various statistical measures and correlations
    3. Visualization: Creates different types of plots and charts for data exploration
    4. Reporting: Generates formatted reports summarizing the findings
    
    The implementation emphasizes interactivity, allowing users to select variables, time periods,
    and analysis methods according to their specific interests and needs.
    """
    elements.append(Paragraph(tech_details_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # Usage Instructions
    elements.append(Paragraph("5. Usage Instructions", styles['Heading2']))
    usage_text = """
    To use the Weather Data Analysis application:
    
    1. Run the application using the provided run.py script: python run.py
    2. The Streamlit web interface will open automatically in your default browser
    3. Navigate through the different sections using the headings
    4. Use the interactive controls (dropdowns, selectors) to customize your analysis
    5. Explore visualizations and statistics for different variables
    6. Download the summary report as a PDF using the download button in the Summary section
    
    The application is designed to be intuitive and user-friendly, with clearly labeled controls
    and organized sections. Users can explore the data at their own pace, moving between different
    types of analyses as needed.
    """
    elements.append(Paragraph(usage_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # Future Enhancements
    elements.append(Paragraph("6. Future Enhancements", styles['Heading2']))
    future_text = """
    Several potential enhancements could further improve the Weather Data Analysis application:
    
    • Predictive modeling capabilities to forecast weather patterns
    • Geospatial visualization to show regional weather variations
    • Integration with real-time weather APIs for current data comparison
    • More advanced statistical analyses and hypothesis testing
    • Enhanced report customization options
    • Ability to upload and analyze custom weather datasets
    
    These enhancements would expand the application's functionality and make it more versatile
    for different use cases, from educational purposes to professional weather analysis.
    """
    elements.append(Paragraph(future_text, styles['Normal_Justified']))
    elements.append(Spacer(1, 0.1*inch))
    
    # Conclusion
    elements.append(Paragraph("7. Conclusion", styles['Heading2']))
    conclusion_text = """
    The Weather Data Analysis application provides a comprehensive platform for exploring and
    understanding historical weather data. Through interactive visualizations and statistical
    analyses, it enables users to uncover patterns, correlations, and trends that might not
    be immediately apparent in the raw data.
    
    The application demonstrates the power of data analysis in meteorology, showing how statistical
    techniques and visualizations can transform raw weather measurements into meaningful insights.
    Whether for educational purposes, research, or personal interest, this tool offers valuable
    capabilities for weather data exploration.
    
    By combining robust data processing with an intuitive user interface, the application makes
    complex data analysis accessible to users with varying levels of technical expertise, promoting
    a deeper understanding of weather patterns and climate dynamics.
    """
    elements.append(Paragraph(conclusion_text, styles['Normal_Justified']))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

# Create the download button for project documentation
if __name__ == "__main__":
    st.set_page_config(page_title="Weather Data Analysis Documentation", layout="wide")
    
    st.title("Weather Data Analysis Project Documentation")
    st.markdown("""
    This page provides detailed documentation for the Weather Data Analysis project.
    Click the button below to download the complete project documentation as a PDF file.
    """)
    
    # Generate and offer the documentation for download
    doc_pdf = generate_project_documentation()
    st.download_button(
        label="📥 Download Project Documentation",
        data=doc_pdf,
        file_name="weather_data_analysis_documentation.pdf",
        mime="application/pdf",
    )