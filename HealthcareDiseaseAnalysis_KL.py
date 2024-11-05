# Public API found from: https://clinicaltables.nlm.nih.gov/apidoc/disease_names/v3/doc.html

import streamlit as st
from openai import OpenAI
import json
import pandas as pd
import requests # for additional API calls
import matplotlib.pyplot as plt

# Set your OpenAI API key here
client = OpenAI(api_key="your_api_key_here")

# New function to fetch additional disease data from a public API
def get_additional_disease_data(disease_name):
    url = f"https://clinicaltables.nlm.nih.gov/api/disease_names/v3/search?terms={disease_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.warning(f"Additional data for {disease_name} not found.")
        return None


def get_disease_info(disease_name):
    """
    Function to query OpenAI and return structured information about a disease.
    """
    medication_format = '''"name":""
    "side_effects":[
    0:""
    1:""
    ...
    ]
    "dosage":""'''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Please provide information on the following aspects for {disease_name}: 1. Key Statistics, 2. Recovery Options, 3. Recommended Medications. Format the response in JSON with keys for 'name', 'statistics', 'total_cases' (this always has to be a number), 'recovery_rate' (this always has to be a percentage), 'mortality_rate' (this always has to be a percentage) 'recovery_options', (explain each recovery option in detail), and 'medication', (give some side effect examples and dosages) always use this json format for medication : {medication_format} ."}
        ]
    )
    return response.choices[0].message.content

# Adjusted to display both disease info and additional disease data
def display_disease_info(disease_info, additional_data = None):
    """
    Function to display the disease information in a structured way using Streamlit.
    """
    try:
        info = json.loads(disease_info)

        recovery_rate = float(info['statistics']["recovery_rate"].strip('%'))
        mortality_rate = float(info['statistics']["mortality_rate"].strip('%'))
        rates = [recovery_rate, mortality_rate]   # 1d array to display a pie chart

        chart_data = pd.DataFrame(
            {
                "Recovery Rate": [recovery_rate],
                "Mortality Rate": [mortality_rate],
            },
            index = ["Rate"]  # This is a single index. You might adjust it based on your data structure.
        )

        # Display additional data if available
        if additional_data:
            st.divider()
            st.subheader(f":blue[Various Medical Conditions related to *'{info['name']}'*]")
            # Keep only the text 
            clean_data = [data[0] for data in additional_data[3]]
            for data in clean_data:
                st.write(f"- {data}")
            st.divider()
        
        st.subheader(f":blue[Recovery rate vs Mortality rate of *{info['name']}*]")
        # Pie chart more suitable than the bar chart to display the Mortality vs Recovery rates 
        fig1, ax1 = plt.subplots()
        colors = ['Cyan','Red']
        ax1.pie(x=rates, explode=None, labels=['Recovery Rate' , 'Mortality Rate'], colors=colors, autopct='%1.1f%%', textprops={'fontsize': 10})
        ax1.axis('equal')  
        st.pyplot(fig1)  
        st.divider()
        
        st.subheader(":blue[Recovery Options]")
        recovery_options = info['recovery_options']
        for option, description in recovery_options.items():
            st.write(f"**{option}**: {description}")
        st.divider()
        
        st.subheader(":blue[Recommended Medication]")
        medication = info['medication']
        # medication_count = 1
        for option, description in medication.items():
            st.write(f"**{option}**: {description}")
            # medication_count += 1
        st.divider()
    
    except json.JSONDecodeError:
        st.error("Failed to decode the response into JSON. Please check the format of the OpenAI response.")

st.title("Disease Information Dashboard")

# Add an explanation for the user and placeholder text
st.write("Enter the name of a disease to get detailed information including statistics, recovery options, and recommended medications.")
disease_name = st.text_input("Enter the name of the disease:", placeholder = "e.g., COVID-19")

if disease_name:
    with st.spinner('Fetching disease data...'):
        disease_info = get_disease_info(disease_name)
        
        # Fetch additional disease data from a public API
        additional_data = get_additional_disease_data(disease_name)
        
        # Pass additional data to display function
        display_disease_info(disease_info, additional_data = additional_data)
        
        # Add option to download the disease info as a json file
        if st.checkbox('**Download Data as JSON**'):
            st.markdown('**Press the button to download the above data as a json file.**')
            st.download_button(label = "Download JSON", data = disease_info, file_name = f"{disease_name}_info.json", mime = "application/json", type='primary')
else:
    st.write("Please enter a disease name to retrieve information.")