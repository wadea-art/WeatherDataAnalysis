# Weather Data Analysis Application

A comprehensive tool for analyzing historical weather data with interactive visualizations and statistical insights.

![Weather Data Analysis](https://raw.githubusercontent.com/your-username/weather-data-analysis/main/screenshot.png)

## Overview

This Weather Data Analysis application provides a complete solution for exploring and understanding weather patterns from historical data. The application processes raw weather measurements and presents them through an intuitive interface with interactive visualizations and detailed statistical analysis.

## Features

- **Data Overview**: Basic information about the dataset and sample data display
- **Basic Statistics**: Key statistical measures for all weather variables
- **Univariate Analysis**: Distribution analysis of individual variables
- **Time Series Analysis**: Trends and patterns over different time periods
- **Bivariate Analysis**: Relationship exploration between weather variables
- **Key Weather Questions**: Answers to important meteorological questions
- **Summary Report**: Comprehensive report with downloadable PDF option

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Required Python packages: 
  - streamlit
  - pandas
  - matplotlib
  - seaborn
  - numpy
  - scipy
  - reportlab

### Installation

1. Clone this repository or download the source code
2. Make sure you have the weather data CSV file in the `attached_assets` directory
3. Install required packages:

```bash
pip install streamlit pandas matplotlib seaborn numpy scipy reportlab
```

### Running the Application

#### Using the Shell Script (Recommended)

The easiest way to run the application is using the provided shell script:

```bash
# Make the script executable
chmod +x run_weather_analysis.sh

# Run the script
./run_weather_analysis.sh
```

This will display a menu with options to:
1. Run the Weather Data Analysis Application
2. Generate PDF Documentation
3. View Help Information
4. Exit

#### Using Python Directly

Alternatively, you can run the application directly with Python:

```bash
# Run the main application
python run.py

# Or to generate documentation
python run.py --docs
```

## Documentation

Detailed documentation is available in two formats:

- **User Documentation** (`DOCUMENTATION.md`): Comprehensive guide to all features of the application
- **Technical Documentation** (`CODE_DOCUMENTATION.md`): Detailed explanation of the code structure and implementation

## Project Structure

```
.
├── attached_assets/      # Data directory
│   └── weatherHistory.csv  # Main weather dataset
├── weather_app.py        # Main Streamlit application
├── data_processing.py    # Data loading and cleaning
├── visualization.py      # Visualization components
├── analytics.py          # Statistical analysis
├── reporting.py          # Report generation
├── run.py                # Python runner script
├── run_weather_analysis.sh  # Bash runner script
└── documentation files
```

## Weather Data

The application works with historical weather data in CSV format. The dataset should include:
- Temperature measurements
- Humidity readings
- Wind speed and direction
- Atmospheric pressure
- Visibility
- Date and time information

## Contributing

Contributions to improve the application are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Weather data provided by [source of your weather data]
- Built with Streamlit, Pandas, Matplotlib, and other open-source libraries

---

*This application was created as a data analysis project to provide insights into historical weather patterns.*