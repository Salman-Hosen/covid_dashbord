import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
@st.cache
def load_data(file_path):
    """Load data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# Load your dataset
file_path = "https://raw.githubusercontent.com/Salman-Hosen/covid_dashbord/main/country_wise_latest.csv"
data = load_data(file_path)

# Set up Streamlit
st.title("COVID-19 Data Dashboard")
st.sidebar.title("Navigation Menu")

# Navigation Menu
menu = st.sidebar.radio("Select an Option", ["View Data", "Search Data", "Visualize Data"])

# View Data Section
if menu == "View Data":
    st.header("Explore the Dataset")
    st.write("Below is the dataset loaded for analysis:")
    st.dataframe(data)

    # Download Option
    if not data.empty:
        csv = data.to_csv(index=False)
        st.download_button("Download Data as CSV", csv, file_name="filtered_data.csv")

# Search Data Section
if menu == "Search Data":
    st.header("Search Data")
    search_country = st.text_input("Enter Country Name to Search:")

    if search_country:
        if not data.empty:
            filtered_data = data[data['Country/Region'].str.contains(search_country, case=False, na=False)]
            if not filtered_data.empty:
                st.write(f"Search Results for '{search_country}':")
                st.dataframe(filtered_data)
            else:
                st.write(f"No results found for '{search_country}'.")
        else:
            st.write("Dataset is empty. Please check your data source.")

# Visualize Data Section
if menu == "Visualize Data":
    st.header("Visualize Data")
    if not data.empty:
        graph_type = st.selectbox("Select Graph Type", ["Pie Chart", "Bar Chart", "Line Chart"])

        # Select Column for Visualization
        column = st.selectbox("Select Column to Visualize", data.columns[1:])

        if graph_type == "Pie Chart":
            top_n = st.slider("Select Number of Top Countries to Display", min_value=5, max_value=20, value=10)
            sorted_data = data.sort_values(column, ascending=False).head(top_n)
            fig, ax = plt.subplots()
            ax.pie(sorted_data[column], labels=sorted_data['Country/Region'], autopct='%1.1f%%', startangle=140)
            ax.set_title(f"Top {top_n} Countries by {column}")
            st.pyplot(fig)

        elif graph_type == "Bar Chart":
            top_n = st.slider("Select Number of Top Countries to Display", min_value=5, max_value=20, value=10)
            sorted_data = data.sort_values(column, ascending=False).head(top_n)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(sorted_data['Country/Region'], sorted_data[column], color='skyblue')
            ax.set_title(f"Top {top_n} Countries by {column}")
            ax.set_xlabel('Country')
            ax.set_ylabel(column)
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

        elif graph_type == "Line Chart":
            st.line_chart(data[column])
    else:
        st.write("Dataset is empty. Please check your data source.")

# Footer
st.sidebar.write("---")
st.sidebar.write("Developed by Salman")
