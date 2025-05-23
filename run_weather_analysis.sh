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
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch

print("Generating comprehensive project documentation...")

# Create the PDF document
doc = SimpleDocTemplate("weather_data_analysis_documentation.pdf", 
                       pagesize=letter,
                       rightMargin=0.5*inch, 
                       leftMargin=0.5*inch,
                       topMargin=0.5*inch, 
                       bottomMargin=0.5*inch)

# Get styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    name='DocTitle',
    parent=styles['Heading1'],
    fontSize=18,
    alignment=TA_CENTER,
    spaceAfter=12
)
heading2_style = ParagraphStyle(
    name='DocHeading2',
    parent=styles['Heading2'],
    fontSize=16,
    spaceAfter=10
)
normal_style = ParagraphStyle(
    name='DocNormal',
    parent=styles['Normal'],
    alignment=TA_JUSTIFY,
    spaceAfter=8
)

# Content for the document
elements = []

# Title
elements.append(Paragraph("Weather Data Analysis Project Documentation", title_style))
elements.append(Spacer(1, 0.2*inch))

# Overview section
elements.append(Paragraph("1. Project Overview", heading2_style))
overview_text = """
The Weather Data Analysis application is a Python-based tool designed to process and analyze 
historical weather data from multiple sources. It offers an interactive interface for exploring 
weather patterns, performing statistical analysis, and generating visualizations to better 
understand climate trends and relationships between different weather variables.
"""
elements.append(Paragraph(overview_text, normal_style))
elements.append(Spacer(1, 0.1*inch))

# Features section
elements.append(Paragraph("2. Key Features", heading2_style))
features_text = """
The application includes the following key features:

• Data Loading and Cleaning: Process raw weather data from CSV files, handle missing values, 
  and prepare it for analysis.

• Basic Statistics: Calculate and display fundamental statistical measures for weather variables 
  including mean, median, standard deviation, and range.

• Univariate Analysis: Examine the distribution and characteristics of individual weather 
  variables through histograms, box plots, and detailed statistics.

• Time Series Analysis: Analyze how weather variables change over time using various time 
  aggregation levels (day, month, year) and identify seasonal patterns.

• Bivariate Analysis: Explore relationships between pairs of weather variables through scatter 
  plots, correlation coefficients, and heat maps.

• Key Weather Questions: Answer specific meteorological questions such as seasonal temperature 
  patterns and the relationship between temperature and humidity.

• Report Generation: Create downloadable PDF reports summarizing the findings and insights 
  from the weather data analysis.
"""
elements.append(Paragraph(features_text, normal_style))
elements.append(Spacer(1, 0.1*inch))

# Technical details
elements.append(Paragraph("3. Technical Implementation", heading2_style))
tech_text = """
The application is built using several Python libraries and technologies:

• Streamlit: Provides the web-based interactive interface
• Pandas: Handles data loading, manipulation, and analysis
• Matplotlib and Seaborn: Create data visualizations
• NumPy: Perform numerical computations
• ReportLab: Generate PDF reports

The application follows a modular structure with components for data processing, analysis, 
visualization, and reporting.
"""
elements.append(Paragraph(tech_text, normal_style))
elements.append(Spacer(1, 0.1*inch))

# Usage section
elements.append(Paragraph("4. Usage Instructions", heading2_style))
usage_text = """
To use the Weather Data Analysis application:

1. Run the application using the provided script: ./run_weather_analysis.sh
2. Select option 1 from the menu to start the main application
3. The web interface will open in your browser at http://localhost:5000
4. Use the interactive controls to select variables for analysis
5. Explore the different tabs for various types of analysis
6. Download reports or visualizations as needed

The application provides an intuitive interface with different sections for exploring various
aspects of the weather data.
"""
elements.append(Paragraph(usage_text, normal_style))
elements.append(Spacer(1, 0.1*inch))

# Build the PDF
doc.build(elements)
print("Documentation generated successfully!")
print("File saved as: weather_data_analysis_documentation.pdf")
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