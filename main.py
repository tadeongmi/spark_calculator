import streamlit as st
import pandas as pd
import locale

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

def pretty_number(number):
    formatted_string = '{:,.2f} USD'.format(number)
    return formatted_string

def pretty_usd(df,amount_collateral,selected_collateral):
    number = df[df['underlying_symbol'] == selected_collateral]['price'].values[0]*amount_collateral
    return pretty_number(number)





# frontend
def home():
    st.title('⚡️ Spark Calculator ⚡️')
    st.caption('A simple calculator for SparkLend to help calculate the liquidation price of a position.')

    df = get_market_data()
    st.write(df)

    selected_network = st.selectbox('select network', available_markets(df))

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        selected_collateral = st.selectbox('select collateral asset', available_collaterals(df,selected_network))
        # st.write(df[(df['underlying_symbol'] == selected_collateral) & (df['network'] == selected_network)]) # TODO delete

    with col2:
        amount_collateral = st.number_input('enter collateral amount', value=0.0, step=0.01, format="%.2f", min_value=0.0)
        usd_collateral_value = pretty_usd(df,amount_collateral,selected_collateral)
        st.write(usd_collateral_value)

    with col3:
        selected_borrow = st.selectbox('select borrow asset', available_borrows(df,selected_network))
        # st.write(df[(df['underlying_symbol'] == selected_borrow) & (df['network'] == selected_network)]) # TODO delete

    with col4:
        amount_borrow = st.number_input('enter borrow amount', value=0.0, step=0.01, format="%.2f", min_value=0.0)
        usd_borrow_value = pretty_usd(df,amount_collateral,selected_collateral)
        st.write(usd_borrow_value)


def about():
    st.title('About')
    # Add content for the about page

def contact():
    st.title('Contact')
    # Add content for the contact page

pages = {
    'Home': home,
    'About': about,
    'Contact': contact
}

selected_page = st.sidebar.radio('Navigation', list(pages.keys()))

pages[selected_page]()
