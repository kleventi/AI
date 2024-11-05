# AI summer school assignments
-----------------------------------------------------
# FinancialAnalysis.py
## Create a Streamlit Application that by inputting 2 different stock tickers you can use OpenAI LLM to do a comparative analysis between their stock progress of a set date. The user can specify the start and end dates for the data they wish to fetch.
- Integrate yfinance for Financial Data
yfinance is a Python library that can access the financial data available on Yahoo Finance. It's capable of fetching historical market data, real-time data, and financials information, among other data types.
- Fetch Stock Data with yfinance
- Display Stock Data in the Streamlit App
- Integrate OpenAI for generating comparative stock performance analysis.
- Create and visually present charts for the 2 different stocks. The user can select from a list of different chart types.
-----------------------------------------------------
# HealthcareDiseaseAnalysis.py
## Create a User Interface application with the help of Streamlit and OpenAI to get an analysis on a diseases based on user input.
- Set up the OpenAI API key to authenticate requests
- Create a basic Interface with a title and a text_input that the user will be able to add any disease to the application
- Create a function to query OpenAI's API (https://clinicaltables.nlm.nih.gov/api/disease_names/v3/search?terms={disease_name}) and get structured information about a disease. This function will take the disease name as input and return detailed information about the disease
- Parse the JSON Data
- Extract and Convert Statistics
- Create a DataFrame for Visualization
- Display the Statistics
- Display Recovery Options
- Display Medication Information
-----------------------------------------------------
# QuizGenerator.py
## Build an interactive quiz application using Streamlit and OpenAI. This application will display questions, check answers, and provide feedback. Additionally, generate new questions dynamically by using OpenAI.
- Creating Classes for Questions and Quiz
- Loading or Generating Questions
- Initializing Session State
- Displaying the Quiz
- Displaying the Current Question
- Checking the Answer
- Displaying Results
- Updating the Progress Bar
- Restarting the Quiz
- Generating New Questions with OpenAI
-----------------------------------------------------
# DataAssignmentWithPython.py
## Data Assignment with Python: Liquor Sales Analysis
Project Overview: We are provided with a dataset detailing Liquor Sales in Iowa, USA, spanning the years 2012-2020.
Dataset Link: https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv

The tasks at hand are, for the timeframe 2016-2019:
- Discern the most popular item in each zipcode and
- Compute the sales percentage per store (in dollars).

Objectives:
- Data Extraction and Cleaning: Extract pertinent data and conduct preliminary cleaning to handle missing or inconsistent data.
- Data Analysis: Employ Python with Pandas or SQL to analyze the dataset, identifying the predominant item per zipcode and calculating the proportion of sales for each store between 2016 and 2019.
- Data Visualization: Represent the analyzed data aesthetically and informatively using tools like matplotlib, seaborn, plotly, or integrate with visualization platforms such as Tableau Public, Power BI, Looker Studio, or HEX for a more interactive experience.

Deliverables:
- Analytical Report: A comprehensive report detailing the methodologies used, the analysis performed, and the insights derived as well as the code.
- Visualization Dashboard: An interactive dashboard or a set of plots/graphs using one of the prescribed tools, encapsulating the key findings and insights.

Workflow:
- Data Preparation: Extract, clean, and prepare the dataset for analysis.
- Exploratory Data Analysis (EDA): Explore the dataset to understand its structure, trends, and patterns.
- Data Manipulation: Use Python and Pandas for data transformation and computation to derive insights.
- Visualization and Presentation: Present the results in a visually appealing and informative manner using suitable visualization tools.
-----------------------------------------------------

