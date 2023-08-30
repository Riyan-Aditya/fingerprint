import streamlit as st 
import pandas as pd
import xlrd
import base64
from io import BytesIO

st.write("""
# Fingerprint absent transpose app

This app transpose the data from fingerprint machine for JR Raynaldi Group

""")

# turn off upload error warning
st.set_option('deprecation.showfileUploaderEncoding', False)

# -----------------------------------------------
# create sidebar
st.sidebar.header('User Input Features')

# Collects user input features into dataframe

# upload xls file
uploaded_file = st.sidebar.file_uploader("Upload your input Excel file", type=["xls","xlsx"])
if uploaded_file is not None:
    input_df = pd.read_excel(uploaded_file, engine = "openpyxl")
    
# select time format
time_format = st.sidebar.selectbox('Time_format:',("%d/%m/%Y %H:%M","%m/%d/%Y %H:%M","%m/%d/%Y %I:%M %p","%d/%m/%Y %H.%M"))

# create button to run function
run_funct = st.sidebar.button('Run function')

# -----------------------------------------------
# Fingerprint transpose function
def fingerprint_transpose(input_df, time_format):
    df2 = input_df.copy()
    df2['Waktu'] = pd.to_datetime(df2['Waktu'], format =time_format)
    df2['Tanggal'] = df2['Waktu'].dt.strftime('%d/%m/%Y')
    df2['Jam'] = df2['Waktu'].dt.strftime('%H:%M')
    df2 = df2[['Nama','No. ID','Tanggal','Jam','Status']]
    
    xxx = df2.sort_values(['Nama','Tanggal', 'Jam'], ascending=[True,True,True])
    yyy = xxx.groupby(['Nama','Tanggal','Jam'])['Status'].count()
    yy = yyy.copy()
    zz = yy.reset_index()
    zz = zz.drop('Status', axis = 1)

    group = zz.groupby(['Nama','Tanggal'])
    dfzz = group.apply(lambda x: x['Jam'].unique())
    dfzz = dfzz.apply(pd.Series)
    dfzz = dfzz.reset_index()
    
    return dfzz
    
    #global result_file_name
    #result_file_name = "fingerprint_result.xlsx"
    #writer = pd.ExcelWriter(result_file_name,  datetime_format='hh:mm')
    #dfzz.to_excel(writer, "Sheet1")
    #writer.close()
    #print('done')

# function to download excel. 
# taken from: https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/12
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download csv file</a>' # decode b'abc' => abc

   

# -----------------------------------------------
# Displays the user input features
st.subheader('Input file')
if uploaded_file is not None:
    st.write(input_df.head(2))
    st.write('')
    st.write(input_df.Waktu[0])

st.subheader('Time format yang dipilih')
if time_format is not None:
    st.write(time_format)

st.subheader('Preview and Download result')

if run_funct == True:
    df = fingerprint_transpose(input_df, time_format)
    st.write(df.head(3))
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)
    st.write('Selesai. Silahkan klik kanan dan save link di atas')
