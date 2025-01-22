import streamlit as st
import pandas as pd

# Setting the title of the web page
st.set_page_config(page_title="CATS (2022-24) Running Vehicle Pricing Guide")
#st.set_page_config(layout="wide")

# Displaying the formatted title on the app page
st.title("CATS (2022-24) Running Vehicle Pricing Guide")
st.header("Year: 1995-2015")

# Load data
@st.cache_data
def load_data():
    path = 'Yearly Pricing Book_Main.xlsx'
    return pd.read_excel(path)

df = load_data()

# Convert 'Year' to string to prevent formatting with commas
df['Year'] = df['Year'].astype(str)

# Standardizing text fields with the first letter capitalized
df['Make'] = df['Make'].str.capitalize()
df['Model'] = df['Model'].str.capitalize()

# Sorting values
df.sort_values(by=['Year', 'Make', 'Model'], ascending=[True, True, True], inplace=True)

# Sidebar - Year, Make, Model selection
year = st.sidebar.selectbox('Select Year:', [''] + sorted(df['Year'].unique()), index=0, format_func=lambda x: 'Select Year' if x == '' else x)
make = st.sidebar.selectbox('Select Make:', [''] + sorted(df[df['Year'] == year]['Make'].unique()), index=0, format_func=lambda x: 'Select Make' if x == '' else x)
model = st.sidebar.selectbox('Select Model:', df[(df['Year'] == year) & (df['Make'] == make)]['Model'].unique())

# Main container for displaying results
with st.container():
    # Apply filters only if selections are made
    if year and make and model:
        filtered_data = df[(df['Year'] == year) & (df['Make'] == make) & (df['Model'] == model)]

        # Adding a new serial number column starting from 1
        filtered_data = filtered_data.reset_index(drop=True)
        filtered_data.index = filtered_data.index + 1
        filtered_data.index.name = 'S.No'

        # Displaying results
        if not filtered_data.empty:
            average_price = round(filtered_data['Sold Price'].mean())
            sample_size = filtered_data.shape[0]

            st.write(f"Average Sold Price: ${average_price}")
            st.write(f"Sample Size: {sample_size}")
            st.write("Complete List of Samples:")
            st.dataframe(filtered_data)
        else:
            st.write("No data available for the selected vehicle.")
    else:
        st.write("Please select year, make, and model to see data.")
