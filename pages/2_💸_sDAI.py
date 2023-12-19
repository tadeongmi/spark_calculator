import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='sDAI Accountant',
    page_icon='spark_logo.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# backend
@st.cache_data
def get_dsr_rate():
    df = pd.read_csv('pot_dsr.csv')
    return df

@st.cache_data
def get_sdai_transfers():
    df = pd.read_csv('example_sdai.csv')
    return df

# utils
def pretty_percent(percent):
    formatted_string = '{:,.2f}%'.format(percent * 100)
    return formatted_string

# frontend
def main():
    st.title('💸 sDAI Accountant 💸')
    
    col01, col02 = st.columns([3,1])
    with col01:
        st.caption('A little helper to know the effective yield in amount and percentage of yout sDAI after mutliple operations')

    with col02:
        st.caption('data updated on 19th Dec 2023')

    st.write("") # space

    df_dsr = get_dsr_rate()

    df_transfers = get_sdai_transfers()

    col1, col2 = st.columns(2)
    with col1:
        st.write(df_dsr)
    with col2:
        st.write(df_transfers)


    # Creating the DataFrame


    st.download_button('Download historical DSR rate', data=df_dsr.to_csv(), file_name='pot_dsr.csv', mime='text/csv')

    # Convert DSR data to DataFrame
    df_dsr['datetime'] = pd.to_datetime(df_dsr['datetime'])
    df_dsr.set_index('datetime', inplace=True)
    df_dsr.index = df_dsr.index.tz_localize(None)
    dsr_daily = df_dsr.resample('D').ffill()

    # Resample DSR DataFrame to daily frequency
    #dsr_daily = dsr_daily.reindex(df_transfers.index, method='ffill')

    st.write(dsr_daily.head(10))

################################################################################################

'''
 df_transfers['date'] = pd.to_datetime(df_transfers['date'])
    df_transfers = df_transfers.sort_values(by='date')
    df['daily_balance'] = df['amount'].cumsum()
    df_transfers.set_index('date', inplace=True)
    df_transfers_daily = df_transfers.resample('D').last()
    df_transfers_daily['daily_balance'].fillna(method='ffill', inplace=True)
    df_transfers_daily['amount'].fillna(0, inplace=True)
    df_transfers_daily.reset_index(inplace=True)

    st.write(df_transfers_daily.head(10))
'''


'''
    df_transfers['date'] = pd.to_datetime(df['date'])
    df_transfers = df_transfers.sort_values(by='date')
    df_transfers.set_index('date', inplace=True)
    df_transfers['daily_balance'] = df_transfers['amount'].cumsum()
    df_transfers['daily_return'] = df_transfers['daily_balance'] * dsr_daily['rate'] / 365
    df_transfers['cumulative_return'] = df_transfers['daily_return'].cumsum()
'''

# app
if __name__ == '__main__':
    main()