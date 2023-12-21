import streamlit as st
import pandas as pd

# TODO:
# - [ ] add a file uploader for common file formats (maybe Safe or Etherscan?)
# - [ ] get dsr rate from api
# - [ ] add amounts in sDAI
# - [ ] add breakeven calculation


st.set_page_config(
    page_title='sDAI Calculator',
    page_icon='spark_logo.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# backend
@st.cache_data
def get_dsr_rate():
    df_dsr = pd.read_csv('pot_dsr.csv')
    df_dsr['datetime'] = pd.to_datetime(df_dsr['datetime'])
    df_dsr['datetime'] = df_dsr['datetime'].dt.date
    return df_dsr

def process_user_transactions(df_transactions):
    df_transactions['date'] = pd.to_datetime(df_transactions['date'])
    df_dates = pd.DataFrame(pd.date_range(start=df_transactions['date'].min(), end=pd.to_datetime('today')), columns=['date'])
    df_daily = pd.concat([df_transactions, df_dates], axis=0, ignore_index=True)
    df_daily.sort_values('date', inplace=True)
    df_daily['balance'] = df_daily['amount'].cumsum()
    df_daily.drop(columns=['amount'], inplace=True)
    df_daily['balance'].fillna(method='ffill', inplace=True)
    df_daily['date'] = df_daily['date'].dt.date
    df_daily = df_daily.drop_duplicates(subset='date', keep='last')
    return df_daily

def calculate_return(df_daily, df_dsr):
    df_merged = pd.merge(df_daily, df_dsr, how='outer', left_on='date', right_on='datetime')
    df_merged['date'] = df_merged['date'].combine_first(df_merged['datetime'])
    df_merged.drop('datetime', axis=1, inplace=True)
    df_merged.sort_values(by='date', inplace=True)
    df_merged['rate'].fillna(method='ffill', inplace=True)
    df_merged.dropna(subset=['balance'], inplace=True)
    df_merged['apr'] = (1 + df_merged['rate'])**(1/365) - 1
    df_merged['return'] = df_merged['balance'] * df_merged['apr']
    return df_merged

# utils
def pretty_percent(percent):
    formatted_string = '{:,.2f}%'.format(percent * 100)
    return formatted_string

def pretty_number(number):
    try:
        integer_digits = len(str(int(number)))
        if integer_digits > 2:
            return '{:,.2f}'.format(number)
        else:
            return '{:,.4f}'.format(number)
        return formatted_string
    except:
        return '{:,.2f}'.format(number)
    
def pretty_dai(number):
    formatted_string = '{:,.2f} DAI'.format(number)
    return formatted_string

# frontend
def main():
    st.title('💸 sDAI Calculator 💸')
    
    col01, col02 = st.columns([3,1])
    with col01:
        st.caption('A simple calculator to know the effective yield of your sDAI.')

    with col02:
        st.caption('data updated on 19th Dec 2023')

    st.write('') # space
    success = False # control flow for the bulk of calculations

    # get data
    uploaded_sdai = st.file_uploader('Upload your sDAI transactions', type=['csv'])

    if uploaded_sdai is not None:

        try:
            df_transactions = pd.read_csv(uploaded_sdai)

            try:
                date_column = df_transactions['date']
                amount_column = df_transactions['amount']
                st.success('the csv file has been processed correctly')
                success = True
            except:
                st.warning('the csv file does not contain the correct format, please try using the sample file provided below.')
                success = False

        except:
            st.warning('there was an error, please try to uploading a valid csv file')
            success = False
    
    st.caption('Upload a CSV file with 2 columns, date (yyyy-mm-dd) and amount (DAI amount w/ decimal point, negative when exiting sDAI).')
    with open('example_sdai.csv') as f:
        st.download_button('Download sample sDAI transactions', f, file_name='sample_sdai.csv', mime='text/csv')

    if success is True:
        df_dsr = get_dsr_rate()

        # process data
        df_daily = process_user_transactions(df_transactions)
        df_merged = calculate_return(df_daily, df_dsr)

        st.write('') # space
        st.header('your sDAI yield')
        final_df = st.empty()

        weighted_average_rate = (df_merged['balance'] * df_merged['rate']).sum() / df_merged['balance'].sum()
        weighted_average_APY = (1 + weighted_average_rate / 31536000) ** 31536000 - 1

        col01, col02, col03 = st.columns([1,1,1])
        with col01:
            total_return = df_merged['return'].sum()
            st.metric(label='effective return', value=pretty_dai(total_return))
        with col02:
            st.metric(label='effective APR', value=pretty_percent(weighted_average_rate))
        with col03:
            st.metric(label='effective APY', value=pretty_percent(weighted_average_APY))

        with final_df.container():
            df_merged.rename(columns={'balance':'DAI nominal balance',
                                    'rate':'APY',
                                    'apr':'daily APR',
                                    'return':'daily return',
                                    }, 
                            inplace=True)
            st.write(df_merged)

        st.write('') # space
        cola, colb = st.columns([1,1])
        with cola:
            st.download_button('Download your sDAI calculations', data=df_transactions.to_csv(index=None), file_name='sdai_yield.csv', mime='text/csv')
        with colb:    
            st.download_button('Download historical DSR APY', data=df_dsr.to_csv(), file_name='pot_dsr.csv', mime='text/csv')
    
    else:
        st.write('')

# app
if __name__ == '__main__':
    main()