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