import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Crimes Visualizer",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("<h1 style='text-align: centre; color: blue;'>UK CRIME'S VISUALIZER</h1>",
                unsafe_allow_html=True)

lats_longs = {'avon_somerset' : [51.375801, -2.359904], 'cambridgeshire' : [52.204832514, 0.120166186],
               'durhum' : [54.776100, -1.573300], 'lincolnshire' : [53.234444, -0.538611], 'london' : [51.509865, -0.118092],
               'north_yorkshire' : [53.958332, -1.080278], 'thames_valley' : [51.5074, -0.1278]}



# counties = st.selectbox('Select a County below', list(lats_longs.keys()))

# but = st.button('SHOW')

avon_somerset = st.secrets["avon_somerset"]
cambridgeshire = st.secrets["cambridgeshire"]
durhum = st.secrets["durhum"]
lincolnshire = st.secrets["lincolnshire"]
london = st.secrets["london"]
north_yorkshire = st.secrets["north_yorkshire"] 
thames_valley = st.secrets["thames_valley"]

counties = st.selectbox('Select a County below', list(lats_longs.keys()))


# @st.cache
def county_select(county):
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=counties)
    # path = "C:\\Users\\ATIF SHAIK\\crimes\\{}.csv".format(county)
    crime = pd.DataFrame(data)
    return crime



crime = county_select(counties)
st.markdown("<h4 style='text-align: centre; color: red;'>CRIMES ON MAP</h4>",
            unsafe_allow_html=True)
map_crime = px.scatter_mapbox(crime, lat='Latitude', lon='Longitude', color='Crime type', 
                    title = 'CRIMES ON MAP',
                    color_continuous_scale="Viridis",
                    range_color=(0, 12),
                    mapbox_style="carto-positron",
                    zoom=7.5, center={"lat": lats_longs[counties][0], "lon": lats_longs[counties][1]},
                    opacity=0.5, animation_frame='Month', width=1200,  # Set the width of the figure
                    height=500,)

map_crime.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(map_crime)


st.markdown("<h4 style='text-align: centre; color: red;'>CRIMES WITH INTENSITIES</h4>",
            unsafe_allow_html=True)
intensity = px.density_mapbox(crime, lat='Latitude', lon='Longitude', z='intensity', radius=10, width=1200, height=500,
                    center=dict(lat=lats_longs[counties][0], lon=lats_longs[counties][1]), zoom=7.5, mapbox_style="open-street-map", animation_frame = 'Month', color_continuous_scale=["blue", "yellow"])
st.plotly_chart(intensity)

st.markdown("<hr>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    yearcol1 = st.selectbox('Select Year', [2020, 2021, 2022, 2023], key = 'year1')
    most_common_crime = crime[crime['year'] == yearcol1]['Crime type'].value_counts().keys()[0].upper()
    st.markdown(f"**MOST COMMON TYPE OF CRIME IN {yearcol1} :** <span style='color: cyan;'>{most_common_crime}</span>", unsafe_allow_html=True)
    # st.write(f'MOST COMMON TYPE OF CRIME IN {yearcol1}: ', crime[crime['year'] == yearcol1]['Crime type'].value_counts().keys()[0].upper())

with col2 :
    yearcol2 = st.selectbox('Select Year', [2020, 2021, 2022, 2023], key = 'year2')
    no_crimes = str(crime[crime['year'] == yearcol2]['Crime type'].value_counts().values[0])
    st.markdown(f"**NUMBER OF CRIMES OCCURRED  IN {yearcol2} :** <span style='color: cyan;'>{no_crimes}</span>", unsafe_allow_html=True)
    # st.write(f'NUMBER OF CRIMES OCCURRED  IN {yearcol2} : ', str(crime[crime['year'] == yearcol2]['Crime type'].value_counts().values[0]))

st.markdown("<hr>", unsafe_allow_html=True)

yearcol3 = st.selectbox('Select Year', [2020, 2021, 2022, 2023], key = 'year3')
outcomes = crime[crime['year'] == yearcol3]['Last outcome category'].value_counts().keys()[0].upper()
st.markdown(f"**MOST COMMON OUTCOME OF POLICE INVESTIGATION IN {yearcol3} :** <span style='color: cyan;'>{outcomes}</span>", unsafe_allow_html=True)
# st.write(f'MOST COMMON OUTCOME OF POLICE INVESTIGATION IN {yearcol3}: ', crime[crime['year'] == yearcol3]['Last outcome category'].value_counts().keys()[0].upper())

st.markdown("<hr>", unsafe_allow_html=True)


st.markdown("<h4 style='text-align: centre; color: red;'>CRIME COUNTS IN DIFFERENT MONTHS</h4>",
            unsafe_allow_html=True)
yearcol44 = st.selectbox('Select Year', [2020, 2021, 2022, 2023], key = 'year4')
scat = px.scatter(crime[crime['year'] == yearcol44], x = 'Crime type', y = 'counts', color = 'months', width=1200, height=500)
st.plotly_chart(scat)


st.markdown("<hr>", unsafe_allow_html=True)


col3, col4 = st.columns(2)

with col3:
    yearcol4 = st.selectbox('Select Year', [2020, 2021, 2022, 2023], key = 'year5')
    tot_crime_month = dict(crime[crime['year'] == yearcol4].groupby('months').counts.sum().sort_values(ascending = False))
    first_pair = next(iter(tot_crime_month.items()))
    most_crime = str(first_pair[0])
    st.markdown(f"**MOST CRIMES OCCURRED IN MONTH :** <span style='color: cyan;'>{most_crime}</span>", unsafe_allow_html=True)
    # st.write('MOST CRIMES OCCURRED IN MONTH : ', str(first_pair[0]))

with col4:
    yearcol5 = st.selectbox('Select Year', [2020, 2021, 2022, 2023], key = 'year6')
    ints = str(np.mean(crime[crime['year'] == yearcol5]['intensity']))
    st.markdown(f"**AVG INTENSITY OF CRIMES OCCURRED IN {yearcol5} :** <span style='color: cyan;'>{ints}</span>", unsafe_allow_html=True)
    # st.write(f"AVG INTENSITY OF CRIMES OCCURRED IN {yearcol5}", str(np.mean(crime[crime['year'] == yearcol5]['intensity'])))

st.markdown("<hr>", unsafe_allow_html=True)


st.markdown("<h4 style='text-align: centre; color: red;'>TYPES OF CRIMES AND THEIR DISTRIBUTION</h4>",
            unsafe_allow_html=True)
yearcol6 = st.selectbox('Select Year', [2020, 2021, 2022, 2023], key = 'year7')
pie = px.pie(crime[crime['year'] == yearcol6], names= 'Crime type', values='counts', width=1200, height=500)   # 2021
st.plotly_chart(pie)


st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: centre; color: red;'>MOST COMMON TYPES OF PLACES WHERE CRIMES OCCUR</h4>",
            unsafe_allow_html=True)
yearcol7 = st.selectbox('Select Year', [2020, 2021, 2022, 2023], key = 'year8')
ba = px.bar(pd.DataFrame(crime[crime['year'] == yearcol7].Location.value_counts()[:25]), width=1200, height=700)
# st.dataframe(pd.DataFrame(crime[crime['year'] == yearcol7].Location.value_counts()))
st.plotly_chart(ba)
