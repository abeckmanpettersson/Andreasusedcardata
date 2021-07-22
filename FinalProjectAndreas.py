"""
Name: Andreas Pettersson Beckman
CS602: Section 2
Data: cl_used_cars_7000_sample
URL: Link to your web application online (see extra credit)
Description:
This program ... (a few sentences about your program and the queries and charts)
"""


import pandas as pd
import streamlit as st
import plotly_express as px

st.set_page_config(layout="wide")

# Title of the App
st.title("Craigslist Used Car Filter Application")
st.image("UsedcarHeader.jpeg")
st.subheader("The purpose of this web application is for users to filter in and out used car listings from Craigslist "
             "based on the car characteristics")
st.subheader("Start by reading this:")
st.markdown("Start off by making sure that you have the ""View Data"" button selected. Then find your way to the Preferences Input "
            "sidebar a filter the listings to fit your preferences. If you want to view the data in the dataframe, "
            "keep the View Data button selected, or hide it by selecting Hide Data. On the map you can see the filtered listings,"
            "hover over the marks to view more detailed information about each listing")

@st.cache(allow_output_mutation=True)
def get_data():
    path = r'https://raw.githubusercontent.com/abeckmanpettersson/Andreasusedcardata/main/cl_used_cars_7000_sample.csv'
    return pd.read_csv(path)

df = get_data()
df.dropna(inplace=True)

# df['year'] = df["year"].astype(str).astype(int)
df.year = df.year.astype(int)
df.price = df.price.astype(float)
# df['price'] = df["price"].astype(str).astype(float)
df['manufacturer'] = df['manufacturer'].str.capitalize()
df['model'] = df['model'].str.capitalize()
df['state'] = df['state'].str.upper()
df['condition'] = df['condition'].str.capitalize()
df['type'] = df['type'].str.capitalize()
df['paint_color'] = df['paint_color'].str.capitalize()


df['year'] = pd.to_numeric(df['year'])
df['price'] = pd.to_numeric(df['price'])

# Add a sidebar for filtering
def sidebar_data():

    st.sidebar.header("Preferences Input")

    # Filter for State
    stateS = df['state'].unique()  # Filter out duplicate values
    state_filter_choice = st.sidebar.multiselect("Filter by State", stateS)  # Create the dropdown widget
    if len(state_filter_choice) == 0:   # To make the default value to everything in the dataframe rather than nothing
        state_filter_choice = df['state'].unique()
    else:
        state_filter_choice = state_filter_choice


    # Filter for Manufacturer
    manufacturerS = df['manufacturer'].loc[df.state.isin(state_filter_choice)].unique()
    manufacturer_filter_choice = st.sidebar.multiselect("Filter by Manufacturer:", manufacturerS)
    if len(manufacturer_filter_choice) == 0:
        manufacturer_filter_choice = df['manufacturer'].unique()
    else:
        manufacturer_filter_choice = manufacturer_filter_choice

    # Filter for Model
    modelS = df['model'].loc[df.manufacturer.isin(manufacturer_filter_choice)].unique()
    model_filter_choice = st.sidebar.multiselect("Filter by Model", modelS)
    if len(model_filter_choice) == 0:
        model_filter_choice = df['model'].unique()
    else:
        model_filter_choice = model_filter_choice

    # Filter for Color
    colorS = df['paint_color'].loc[df.model.isin(model_filter_choice)].unique()
    color_filter_choice = st.sidebar.multiselect("Filter by Color:", colorS)
    if len(color_filter_choice) == 0:
        color_filter_choice = df['paint_color'].unique()
    else:
        color_filter_choice = color_filter_choice

    # Filter for minimum manufacturing year using a slider
    # min_year = int(df.year.min())
    # max_year = int(df.year.max())
    year_filter_choiceS = st.sidebar.slider("Results by Minimum Manufacturing Year:", min_value=int(df.year.min()),
                                            max_value=int(df.year.max()))

    # Filter for maximum price using a slider
    price_filter_choiceS = st.sidebar.slider("Results by Maximum Price:", min_value=float(df.price.min()),
                                             max_value='300000', value=float(df.price.max()))


    # Filter by car type
    typeS = df['type'].loc[df.paint_color.isin(color_filter_choice)].unique()
    type_filter_choice = st.sidebar.multiselect("Filter by Car Type:", typeS)
    if len(type_filter_choice) == 0:
        type_filter_choice = df['type'].unique()
    else:
        type_filter_choice = type_filter_choice


    # Filter by car condition
    conditionS = df['condition'].loc[df.type.isin(type_filter_choice)].unique()
    condition_filter_choice = st.sidebar.multiselect("Filter by Condition:", conditionS)
    if len(condition_filter_choice) == 0:
        condition_filter_choice = df['condition'].unique()
    else:
        condition_filter_choice = condition_filter_choice


    # Filter by drive (4wd, 2wd, rwd)
    driveS = df['drive'].loc[df.condition.isin(condition_filter_choice)].unique()
    drive_filter_choice = st.sidebar.multiselect("Filter by Drive:", driveS)
    if len(drive_filter_choice) == 0:
        drive_filter_choice = df['drive'].unique()
    else:
        drive_filter_choice = drive_filter_choice



    sidebar_filtering = df[df.state.isin(state_filter_choice) &
            df.manufacturer.isin(manufacturer_filter_choice) &
            df.model.isin(model_filter_choice) &
            df.paint_color.isin(color_filter_choice) &
            df.type.isin(type_filter_choice) &
            df.drive.isin(drive_filter_choice)]

    sidebar_filtering = sidebar_filtering[sidebar_filtering['year'] >= year_filter_choiceS]
    sidebar_filtering = sidebar_filtering[sidebar_filtering['price'] <= price_filter_choiceS]

    st.subheader("Data")



    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True) #To place radio buttons side-by-side
    filtered_clean_data = sidebar_filtering.filter(['manufacturer', 'model', 'year', 'price', 'type', 'color', 'state',
                                                    'condition', 'posting_date', 'lat', 'long', 'description', 'id'])

    view_data = st.radio("View Data", ("View Data", "Hide Data"))
    if view_data == "View Data":
        sort_by_variable = st.radio("What variable do you want to sort?", ("manufacturer", 'model', 'year', 'price',
                                                                           'type', 'state', 'condition', 'posting_date'))
        sort_order = st.radio("Ascending or Descending?", ("ascending", "descending"))
        if sort_order == "ascending":
            sort_order_choice = True
        else:
            sort_order_choice = False

        filtered_clean_data = filtered_clean_data.sort_values(by=[sort_by_variable], ascending=sort_order_choice,
                                                              na_position='last')
        count_rows = 0
        for index in filtered_clean_data.iterrows():
            count_rows += 1
        st.write("Remaining listings:", count_rows, 'out of', len(df))
        st.dataframe(filtered_clean_data)
    st.balloons()

    return filtered_clean_data
filtered_map = sidebar_data()

# Folium Map
def map(filtered_map):
    from streamlit_folium import folium_static
    import folium

    st.header("Map View")
    #st.subheader("To view map, you need to filter at least one non-numerical value")
    zoom = st.slider("", min_value=0, max_value=30, step=1, value=10)
    folium_map = folium.Map(location=[42.3855, -71.2218], zoom_start=zoom)

    for index, row in filtered_map.iterrows():
        folium.Marker(
            [row['lat'], row['long']],
            tooltip=row['manufacturer'],
            popup=row['description']).add_to(folium_map)


    return folium_static(folium_map)
map(filtered_map)


# Plot data using Plotly
def data_plots():
    # Add a select widget
    st.subheader("Select a Chart")
    chart_select = st.selectbox("charts:",['Scatterplots', 'Boxplot'])

    numeric_columns = filtered_map.select_dtypes(['float', 'int']).columns
    non_numeric_columns = filtered_map.select_dtypes(['object']).columns

    if chart_select == 'Scatterplots':
        st.subheader("Scatterplot Settings")
        x_values = st.selectbox('X axis', options=numeric_columns)
        y_values = st.selectbox('Y values', options=numeric_columns)
        group_by = st.selectbox('Group By:', options=non_numeric_columns)
        plot = px.scatter(data_frame=filtered_map, x=x_values, y=y_values, color=group_by, title="Scatterplot numeric "
                                                                                                 "values grouped by car characteristic")
        # display Chart
        st.plotly_chart(plot)
    elif chart_select =='Boxplot':
        st.subheader("Boxplot Settings")
        x_values = st.selectbox('X axis', options=non_numeric_columns)
        y_values = st.selectbox('Y values', options=numeric_columns)
        plot = px.box(data_frame=filtered_map, x=x_values, y=y_values, title="Numeric values grouped by preference")
        # display Chart
        st.plotly_chart(plot)
    return
data_plots()







