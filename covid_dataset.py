import streamlit as st

# Sample dataset URL
file_path = "https://raw.githubusercontent.com/Salman-Hosen/covid_dashbord/main/country_wise_latest.csv"

@st.cache
def load_data(file_path):
    """Load CSV data using Streamlit's text fetching and parsing capabilities."""
    try:
        # Fetch the CSV content
        import urllib.request
        response = urllib.request.urlopen(file_path)
        content = response.read().decode("utf-8")
        
        # Parse the content into headers and rows
        lines = content.splitlines()
        headers = lines[0].split(",")
        data = [dict(zip(headers, line.split(","))) for line in lines[1:]]
        return headers, data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return [], []

# Load the dataset
headers, data = load_data(file_path)

# Streamlit app
st.title("COVID-19 Data Dashboard")
st.sidebar.title("Navigation Menu")

# Navigation Menu
menu = st.sidebar.radio("Select an Option", ["View Data", "Search Data", "Visualize Data"])

# View Data Section
if menu == "View Data":
    st.header("Explore the Dataset")
    if data:
        st.write("Below is the dataset loaded for analysis:")
        st.write(data)
    else:
        st.write("No data available. Please check your data source.")

# Search Data Section
if menu == "Search Data":
    st.header("Search Data")
    search_country = st.text_input("Enter Country Name to Search:")

    if search_country and data:
        filtered_data = [row for row in data if search_country.lower() in row["Country/Region"].lower()]
        if filtered_data:
            st.write(f"Search Results for '{search_country}':")
            st.write(filtered_data)
        else:
            st.write(f"No results found for '{search_country}'.")
    elif not data:
        st.write("Dataset is empty. Please check your data source.")

# Visualize Data Section
if menu == "Visualize Data":
    st.header("Visualize Data")
    if data:
        graph_type = st.selectbox("Select Graph Type", ["Bar Chart", "Line Chart"])
        column = st.selectbox("Select Column to Visualize", headers[1:])

        if graph_type == "Bar Chart":
            # Create a bar chart
            st.bar_chart([float(row[column]) for row in data if row[column].isdigit()])

        elif graph_type == "Line Chart":
            # Create a line chart
            st.line_chart([float(row[column]) for row in data if row[column].isdigit()])
    else:
        st.write("Dataset is empty. Please check your data source.")

# Footer
st.sidebar.write("---")
st.sidebar.write("Developed by Salman")
