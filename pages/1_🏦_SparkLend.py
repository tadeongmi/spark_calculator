import numpy as np
import pandas as pd
import streamlit as st

#TODO:
# multi collateral
# collateral needed (vs max borrow)
# simulation (e.g. if you opened the position last month, would you have been liquidatied?)
# fee (need to also add loan duration)
# use cases(lending arbitrage w/ expected breakeven, long/short/token farming, for looping need "x5" instead of max ltv)
# add sdai yield

# Set page configuration
st.set_page_config(
    page_title='SparkLend Calculator',
    page_icon='spark_logo.svg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# backend
@st.cache_data
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
    return health_factor.item()

def liquidation_price(df,selected_network,selected_collateral,amount_collateral,selected_borrow,amount_borrow):
    usd_borrow = just_usd(df,amount_borrow,selected_borrow)
    collateral_liq_threshold = liquidation_threshold(df,selected_network,selected_collateral)
    liquidation_price = usd_borrow / (amount_collateral * collateral_liq_threshold)
    return liquidation_price.item()

def max_borrowable_amount(df,selected_network,selected_collateral,amount_collateral,selected_borrow,amount_borrow):
    max_ltv = df[(df['underlying_symbol'] == selected_collateral) & (df['network'] == selected_network)]['ltv'].unique()
    usd_collateral = just_usd(df,amount_collateral,selected_collateral)
    max_borrow = (max_ltv * usd_collateral) / usd_price(df,selected_borrow)
    return max_borrow.item()


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

def usd_price(df,selected_asset):
    return df[df['underlying_symbol'] == selected_asset]['price'].values[0]

def just_usd(df,amount_asset,selected_asset):
    return usd_price(df,selected_asset) * amount_asset

def pretty_usd(df,selected_amount,selected_asset):
    number = just_usd(df,selected_amount,selected_asset)
    formatted_string = '{:,.2f} USD'.format(number)
    return formatted_string



# frontend
def home():
    st.title('SparkLend Calculator')
    
    col01, col02 = st.columns([3,1])
    with col01:
        st.caption('A simple calculator to know liquidation price and maximum borrowable amount.')

    with col02:
        st.caption('data updated on 19th Dec 2023')

    st.write("") # space

    df = get_market_data()

    selected_network = st.selectbox('select network', available_markets(df))

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        selected_collateral = st.selectbox('select collateral asset', available_collaterals(df,selected_network))

    with col2:
        amount_collateral = st.number_input('enter collateral amount', value=0.0, step=1.00, format='%.2f', min_value=0.0)
        usd_collateral_value = pretty_usd(df,amount_collateral,selected_collateral)
        st.write(usd_collateral_value)

    with col3:
        selected_borrow = st.selectbox('select borrow asset', available_borrows(df,selected_network))

    with col4:
        amount_borrow = st.number_input('enter borrow amount', value=0.0, step=1.00, format='%.2f', min_value=0.0)
        # %d %e %f %g %i %u
        usd_borrow_value = pretty_usd(df,amount_borrow,selected_borrow)
        st.write(usd_borrow_value)

    st.write('')
    cola, colb, colc = st.columns(3)

    with colb:
        health_factor = heath_factor(df,selected_network,selected_collateral,amount_collateral,selected_borrow,amount_borrow)
        if health_factor < 1:
            st.metric(label='Health Factor', value=pretty_number(health_factor), delta='liquidated', delta_color='inverse')
        else:
            st.metric(label='Health Factor', value=pretty_number(health_factor))

    with cola:
        liq_price = liquidation_price(df,selected_network,selected_collateral,amount_collateral,selected_borrow,amount_borrow)
        current_price = usd_price(df,selected_collateral)
        drawdown = -(current_price - liq_price) / current_price
        delta_text = pretty_percent(drawdown)+' to liquidation'
        if health_factor < 1:
            st.metric(label='Liquidation Price', value=pretty_number(liq_price), delta='liquidated', delta_color='inverse')
        else:
            st.metric(label='Liquidation Price', value=pretty_number(liq_price), delta=delta_text, delta_color='off')

    with colc:
        max_borrow = max_borrowable_amount(df,selected_network,selected_collateral,amount_collateral,selected_borrow,amount_borrow)
        st.metric(label='Max Borrow Amount', value=pretty_number(max_borrow), help='The max borrowable amount is based on the max LTV rather than the liquidation threshold, creating a buffer to avoid inmediate liquidation.')

# app
if __name__ == '__main__':
    home()
