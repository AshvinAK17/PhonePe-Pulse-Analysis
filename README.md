# PhonePe Pulse Data Analysis & Visualization

An end-to-end data analysis and visualization project using PhonePe Pulse datasets. This project uses **SQL**, **Python**, **Plotly**, and **Streamlit** to uncover insights from digital transaction trends across India. The results are presented via an interactive dashboard with state-wise maps, visual graphs, and detailed business case explorations.

---

## Project Objective

To analyze the digital payments landscape in India through PhonePe Pulse public datasets and provide:
- State-wise transaction trends
- User engagement metrics
- Business case studies
- Insurance growth insights
- Interactive visualizations using choropleth maps and graphs

---

## Features

- India Choropleth Map: State-wise transaction heatmap
- Business Case Insights: Real-world use case visualizations
- Quarterly & Yearly Analysis: Trends across years and quarters
- User Behavior Analysis: Device type, insurance usage, and more
- Interactive Streamlit UI: Dropdowns, radio buttons, and maps

---

## Technologies Used
**Python** - The core programming language used for developing data extraction, transformation, and the Streamlit dashboard.

**MySQL Database** - MySQL is a Relational Database Management System (RDBMS) used to store and manage structured data. SQL (Structured Query Language) is used for creating, inserting, updating, and querying data efficiently.

**Pandas** - A powerful data analysis and manipulation library used for handling tabular data.
To install this package:

    pip install pandas

**mysql-connector-python** - A MySQL database connector for Python officially supported by Oracle. It enables Python scripts to connect to MySQL servers, execute queries, and retrieve results.
To install this package:

    pip install mysql-connector-python
**Streamlit**
Streamlit is an open-source Python library for building and sharing interactive web applications for data science and analytics with minimal effort. It supports rapid prototyping and allows users to download filtered data as CSV directly from the app.
To install this package:

    pip install streamlit

## Installation
1. Clone the Repository

        git clone https://github.com/your-username/phonepe-pulse-analysis.git
        cd phonepe-pulse-analysis

2. Install Dependencies

        pip install -r requirements.txt

3. Run the application:

        streamlit run python AIML_PhonePe_Streamlit.py

### Prerequisites
- Python 3.x installed on your system.
- MySQL installed and set up.
- Streamlit web application sign in

## Usage

1. Set up the database and Load:

- Ensure your dataset is in the correct format and placed in the data directory.
- Ensure your MySQL server is running.
- Launch the Streamlit app:
  Run the following command:

      streamlit run AIML_PhonePe_Streamlit.py

2. Interact with the dashboard:

- In the sidebar, choose between:
  - India Overview (Choropleth Map)
  - Business Case Analyses
- Use dropdowns and radio buttons to filter by year, quarter, or metric.
- Hover over states or bars in charts to view detailed insights.
- Explore multiple data views such as transaction volume, device usage, insurance trends, and more.

### Project Structure

- AIML-PhonePe.ipynb: Jupyter Notebook that contains the complete end-to-end workflow: cloning the PhonePe Pulse GitHub repository, extracting and processing data, loading it into a MySQL database (PhonePe_Pulse), transforming it into pandas DataFrames, and performing detailed data visualizations using Plotly, Seaborn, and Matplotlib.

- AIML_PhonePe_Streamlit.py	: The main Streamlit application file. It connects to the MySQL database, runs business case SQL queries, filters and visualizes the results dynamically, and presents them in an interactive web dashboard with dropdowns, radio buttons, and a choropleth map.

- requirements.txt: List of Python dependencies.
