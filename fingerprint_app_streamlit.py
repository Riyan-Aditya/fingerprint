import streamlit as st 
import pandas as pd

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
uploaded_file = st.sidebar.file_uploader("Upload your input Excel file", type=["xls"])
if uploaded_file is not None:
    input_df = pd.read_excel(uploaded_file, engine="xlrd")
    
# select time format
time_format = st.sidebar.selectbox('Time_format:',("%d/%m/%Y %H:%M","%m/%d/%Y %H:%M","%m/%d/%Y %I:%M %p"))

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
    
    global result_file_name
    result_file_name = "fingerprint_result.xlsx"
    writer = pd.ExcelWriter(result_file_name,  datetime_format='hh:mm')
    dfzz.to_excel(writer, "Sheet1")
    writer.close()
    print('done')

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

st.subheader('Download data')

if run_funct == True:
    fingerprint_transpose(input_df, time_format)
    st.write('Selesai. Silahkan cek folder anda. File name: '+result_file_name)
