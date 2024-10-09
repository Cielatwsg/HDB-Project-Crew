import streamlit as st
import pandas as pd
import numpy as np



st.title('HDB Resale Statistics')


url = ('https://www.hdb.gov.sg/cs/infoweb/residential/selling-a-flat/overview/resale-statistics')


@st.cache_data
def load_data(url):
    data = pd.read_html(url)
    data = data[0]
    #lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data_load_state = st.text('Loading data...')
data = load_data(url)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Avg price by town')
hist_values = np.histogram(data["4-Room"], bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
#room type_to_filter = st.slider('hour', 0, 23, 17)
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

#st.subheader('Map of all pickups at %s:00' % hour_to_filter)
#st.map(filtered_data)
