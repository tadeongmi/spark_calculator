import numpy as np
import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title='Spark Calculator',
    page_icon='spark_logo.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# backend
def get_market_data():
    df = pd.read_csv('assets.csv')
    return df

def available_markets(df):
    return df['network'].unique()

def available_collaterals(df,network):
    return df[(df['usage_as_collateral_enabled'] == True) & (df['network'] == network)]['underlying_symbol'].unique()

def available_borrows(df,network):
    return df[(df['borrowing_enabled'] == True) & (df['network'] == network)]['underlying_symbol'].unique()

def liquidation_threshold(df,selected_network,selected_collateral):
    return df[(df['underlying_symbol'] == selected_collateral) & (df['network'] == selected_network)]['liquidation_threshold'].unique()

def heath_factor(df,selected_network,selected_collateral,amount_collateral,selected_borrow,amount_borrow):
    usd_borrow = just_usd(df,amount_borrow,selected_borrow)
    usd_collateral = just_usd(df,amount_collateral,selected_collateral)
    collateral_liq_threshold = liquidation_threshold(df,selected_network,selected_collateral)
    health_factor = (usd_collateral * collateral_liq_threshold) / usd_borrow
    return np.round(health_factor,2)

# utils
def pretty_number(number):
    formatted_string = '{:,.2f}'.format(number)
    return formatted_string

def pretty_usd(df,selected_amount,selected_asset):
    number = df[df['underlying_symbol'] == selected_asset]['price'].values[0]*selected_amount
    formatted_string = '{:,.2f} USD'.format(number)
    return formatted_string

def just_usd(df,amount_collateral,selected_collateral):
    return df[df['underlying_symbol'] == selected_collateral]['price'].values[0]*amount_collateral

# frontend
def home():
    st.title('⚡️ SparkLend Calculator ⚡️')
    st.caption('A simple calculator for SparkLend to help calculate the liquidation price of a position.')

    df = get_market_data()

    selected_network = st.selectbox('select network', available_markets(df))

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        selected_collateral = st.selectbox('select collateral asset', available_collaterals(df,selected_network))

    with col2:
        amount_collateral = st.number_input('enter collateral amount', value=0.0, step=0.01, format="%.2g", min_value=0.0)
        usd_collateral_value = pretty_usd(df,amount_collateral,selected_collateral)
        st.write(usd_collateral_value)

    with col3:
        selected_borrow = st.selectbox('select borrow asset', available_borrows(df,selected_network))

    with col4:
        amount_borrow = st.number_input('enter borrow amount', value=0.0, step=0.01, format="%.2g", min_value=0.0)
        # %d %e %f %g %i %u
        usd_borrow_value = pretty_usd(df,amount_borrow,selected_borrow)
        st.write(usd_borrow_value)

    health_factor = heath_factor(df,selected_network,selected_collateral,amount_collateral,selected_borrow,amount_borrow)
    hf_diff = health_factor - 1
    st.write(hf_diff)

    cola, colb, colc = st.columns(3)

    with colb:
        st.metric(label="Health Factor", value=health_factor, delta=hf_diff.item())


# app
if __name__ == "__main__":
    home()
